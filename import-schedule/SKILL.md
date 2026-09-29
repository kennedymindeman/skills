---
name: import-schedule
description: Turns a screenshot of a schedule into Google Calendar events after the user confirms the parsed list. Use when a pasted or attached image shows a schedule, itinerary, class or shift timetable, event lineup, or appointment list, and the ask is to add it to the calendar, put these on my calendar, or make events from this.
---

A schedule screenshot is a lossy source: years, time zones, and end times are often missing, and an OCR slip becomes a wrong event on the user's real calendar. So every event is read, listed, and confirmed before anything is written. The confirmation is the gate: no `create_event` call happens until the user approves the exact list.

## 1. Get the image

A `~/.cache/clipaste/shot-*.png` path in the message → run the `paste-screenshot` skill to get the file, then read it. An attached image → read it directly.

## 2. Parse every event

Pull each event into these fields:

- **title**
- **date** - with the year; when the image omits it, take the next occurrence on or after today, marked *(assumed)*. A numeric date like 3/4 is read month-first unless the image shows otherwise, also marked *(assumed)*.
- **start / end** - when only a start is shown, end one hour later, marked *(assumed)*. An event with no times is all-day; a multi-day one keeps its last day as the end date.
- **timezone** - the one the image states; otherwise the primary calendar's time zone, marked as assumed.
- **location** - blank when the image shows none.

Every event visible in the image is on the list. A value that was inferred rather than read is marked *(assumed)*, so the user can see what the image did not say.

## 3. Confirm

Show the parsed events as a numbered table - title, date, start, end, timezone, location - then ask with AskUserQuestion:

- **Create all N events (Recommended)**
- **Fix some first** - the user names the corrections; apply them, show the table again, and ask again.
- **Cancel** - write nothing.

## 4. Create

After the user picks "Create all", call `mcp__claude_ai_Google_Calendar__create_event` once per confirmed event on the primary calendar: `summary` is the title, `startTime` and `endTime` are ISO 8601 local times, `timeZone` is the IANA name (e.g. `America/Chicago`), `location` is passed when set, and all-day events set `allDay: true`.

Report each created event with its link. A failed call is reported by event number with the error; the rest still go ahead, and the failed ones are not retried silently.
