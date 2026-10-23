---
name: mobile-gestures
description: Gesture and touch-interaction rules for native iOS, Android, and mobile web UI. Use when designing, building, reviewing, or auditing a mobile screen that uses swipe actions, long press, sheets, drag to reorder, pinch or zoom, pull to refresh, carousels, tab swiping, back navigation, touch targets, undo or confirmation of destructive actions, or haptics.
---

# Mobile gestures

Rules for how a mobile screen responds to touch. Each rule is tied to a source in `EVIDENCE.md` beside this file; read it when a rule needs justifying or a case is not covered.

## Precedence

This skill loads alongside general design skills (ios-hig-design, impeccable, swiftui-expert-skill, swiftui-pro, and similar). Where one of them disagrees with this skill on gestures, touch targets, sheet dismissal, destructive-action confirmation, or haptics, this skill wins. Follow the other skill on everything else.

## Every gesture is a shortcut

Users reliably know two gestures: tap and vertical scroll. Every other gesture (swipe, long press, drag, pinch, double tap, multi-finger, shake, pull) is a **shortcut**: faster for people who find it, invisible to everyone else. Each shortcut gets two twins:

- A **visible tap path**: a More (ellipsis) button, an Edit mode, a toolbar button, or a menu item that performs the same action.
- An **accessibility action**: `accessibilityAction(named:_:)` in SwiftUI, `semantics { customActions = ... }` in Compose, so screen-reader and switch users reach it without the gesture.

An action that exists only as a gesture is a bug, whatever another skill's examples show.

## Row swipe

- Put destructive actions (Delete, Remove) behind row swipe; that is where users look for them.
- A non-destructive action behind swipe (Pin, Mark read, Save) goes unfound unless it is also in the row's menu or a detail screen. Google's Material 3 `SwipeToDismissBox` sample puts "mark done" on swipe; NN/g advises limiting swipe to destructive actions. Treat the disagreement as a reason to mirror, not as permission to hide.
- Full swipe performs the first action with no second step, and SwiftUI's `swipeActions` turns it on by default (`allowsFullSwipe: true`). Keep full swipe only when that action has undo; otherwise pass `allowsFullSwipe: false`.

## Destructive actions: undo first, confirm rarely

- Common, recoverable actions (delete a message, remove a list item, archive) run immediately and offer **undo**. No alert.
- Confirm only for rare, irreversible actions, or ones that lose data or money (delete account, empty trash, send payment). The confirm button names the action ("Delete account"), styled destructive.
- An undo snackbar or toast that carries an action stays until dismissed, or long enough for a VoiceOver or TalkBack user to reach it. A 4-second timed undo is unreachable for them.

## Sheets

- A sheet supports swipe-down dismissal **and** shows a visible Close, Cancel, or Done button. The grabber alone is missed by many users and unusable with assistive input.
- Swipe-down dismisses without asking, unless the sheet holds unsaved changes; then confirm (Discard / Keep editing). In SwiftUI, `interactiveDismissDisabled(hasChanges)` plus a confirmation dialog.
- On Android, system Back (gesture or button) closes the sheet.

## System gestures own the edges

- Never disable, intercept, or overlay iOS edge-swipe back or Android predictive back with app gestures. Leave their gesture regions free of drag targets and horizontal pans.
- Android: the bottom edge (home and recents gesture) cannot be excluded at all. Side-edge exclusion via `setSystemGestureExclusionRects` is honoured for at most 200dp of vertical extent per edge; use it only for a specific control such as a slider thumb.
- iOS 26 and later: a leading-to-trailing pan **anywhere** in a pushed screen's content can start back navigation (`interactiveContentPopGestureRecognizer`), not just at the edge. A horizontal carousel, chart scrubber, slider, or swipeable card inside a pushed screen needs explicit conflict handling (gesture priority or `require(toFail:)` against that recognizer) and a test that both the pan and back still work.
- Carousels get visible previous and next controls. A carousel never sits inside swipeable tab content (tabs that page horizontally), where the two horizontal gestures fight.

## Drag to reorder

Reordering by drag also has a non-drag path: Move up and Move down actions, a Move to menu, or an Edit mode with explicit position controls. Expose the same actions to accessibility.

## Zoom

- Images, maps, and documents support both pinch and double-tap zoom, plus visible zoom in and zoom out (+/-) buttons.
- On the web, never disable browser zoom: no `user-scalable=no`, and `maximum-scale` no lower than 2 in the viewport meta tag.

## Pull to refresh

Pull to refresh also has a Refresh item in a toolbar or overflow menu, so keyboard, switch, and D-pad users can reload.

## Shake and multi-finger gestures

- Avoid them for app actions. If one is used, give it an on-screen control and a setting that turns the motion trigger off.
- Leave the system's meanings alone: on iOS, three-finger swipe and shake mean undo and redo. Do not redefine them.

## Touch targets

- Minimum hit area: 44x44pt on iOS, 48x48dp on Android, with 8dp or more between adjacent targets. The hit area may extend past the visible glyph.
- Targets at screen edges and corners are larger, about 12mm (roughly 75pt or dp). Center targets can be smaller.
- For audiences with motor impairments (older adults, rehab, accessibility-first apps), aim for about 18mm (roughly 115pt or dp).
- WCAG 2.5.8's 24x24 CSS px is a legal floor, not a design target.

## Reach

Keep frequent actions reachable without strain, and make edge and corner targets bigger. Treat the "thumb zone" heat-map as a hypothesis, not a law: observation data shows people shift grip, prefer the center of the screen, and readily reach a top-left Back button. Placing the primary action at the bottom is fine; banning actions from the top is not justified.

## Haptics

- In SwiftUI, use `sensoryFeedback(_:trigger:)` (iOS 17+), tied to a state change, rather than UIKit feedback generators.
- Play a haptic only for a meaningful outcome (success, failure, a snap into place, crossing a threshold), keep it subtle, and pair it with a visible change. Never use one as the only signal.

## Verify on a device

- Test every gesture on real hardware: simulator mouse drags hide edge conflicts, mis-taps, and reach problems.
- Run each changed flow once with VoiceOver (iOS) or TalkBack (Android) on. With a screen reader on, one-finger swipes move focus, so the app's own swipe gestures do not fire; every action must still be reachable through a visible control or the Actions rotor (VoiceOver) or Actions menu (TalkBack).
