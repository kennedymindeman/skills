---
name: mobile-gestures
description: Gesture and touch-interaction rules for native iOS, Android, and mobile web UI. Use when designing, building, reviewing, or auditing a mobile screen that uses swipe actions, long press, sheets, drag to reorder, pinch or zoom, pull to refresh, carousels, tab swiping, back navigation, touch targets, undo or confirmation of destructive actions, or haptics.
---

# Mobile gestures

Rules for how a mobile screen responds to touch. Each rule is tied to a source in `EVIDENCE.md` beside this file; read it when a rule needs justifying or a case is not covered.

## Precedence

This skill loads alongside general design skills (ios-hig-design, impeccable, swiftui-expert-skill, swiftui-pro, and similar). Where one of them disagrees with this skill on gestures, touch targets, sheet dismissal, destructive-action confirmation, or haptics, this skill wins. Follow the other skill on everything else.

## Every gesture is a shortcut

Treat every gesture other than tap and vertical scroll (swipe, long press, drag, pinch, double tap, multi-finger, shake, pull) as a **shortcut**: gestures have no visible signifier, so they are faster for people who find them and invisible to everyone else. Each shortcut gets two twins:

- A **visible tap path**: a More (ellipsis) button, an Edit mode, a toolbar button, or a menu item that performs the same action.
- An **accessibility action**, so screen-reader and switch users reach it without the gesture: `accessibilityAction(named:_:)` in SwiftUI, `accessibilityCustomActions` in UIKit, `semantics { customActions = ... }` in Compose, `ViewCompat.addAccessibilityAction` in Android Views. The web has no ARIA equivalent; there the visible tap path, as a real `<button>`, covers both twins.

An action that exists only as a gesture is a bug, whatever another skill's examples show.

## Row swipe

- Put destructive actions (Delete, Remove) behind row swipe; that is where users look for them.
- A non-destructive action behind swipe (Pin, Mark read, Save) goes unfound unless it is also in the row's menu or a detail screen. Google's Material 3 `SwipeToDismissBox` sample puts "mark done" on swipe; NN/g advises limiting swipe to destructive actions. Treat the disagreement as a reason to mirror, not as permission to hide.
- Full swipe performs the first action with no second step, and SwiftUI's `swipeActions` turns it on by default (`allowsFullSwipe: true`). Keep full swipe only when that action has undo; otherwise pass `allowsFullSwipe: false`.

## Destructive actions: undo first, confirm rarely

- Common, recoverable actions (delete a message, remove a list item, archive) run immediately and offer **undo**. No alert.
- Confirm only for rare, irreversible actions, or ones that lose data or money (delete account, empty trash, send payment). The confirm button names the action ("Delete account"), styled destructive.
- An undo snackbar or toast that carries an action stays until dismissed, or long enough for a VoiceOver or TalkBack user to reach it. A short timed undo is unreachable for them.

## Sheets

- A sheet supports swipe-down dismissal **and** shows a visible Close, Cancel, or Done button. The grabber alone is missed by many users and unusable with assistive input.
- Swipe-down dismisses without asking, unless the sheet holds unsaved changes; then confirm (Discard / Keep editing).
  - SwiftUI has no swipe-attempt callback: `interactiveDismissDisabled(hasChanges)` only blocks the swipe, so the sheet bounces back and only the Cancel button can show the dialog. To confirm on swipe itself, use UIKit's `UIAdaptivePresentationControllerDelegate.presentationControllerDidAttemptToDismiss(_:)` with `isModalInPresentation = hasChanges`.
- On Android, system Back (gesture or button) closes the sheet. With unsaved changes, a back callback (`PredictiveBackHandler` or `OnBackPressedCallback`) enabled only while the form is dirty shows the same confirmation.

## System gestures own the edges

- Back stays available everywhere. Keep drag targets and horizontal pans out of the screen-edge back regions (iOS edge swipe, Android side edges). The only sanctioned exceptions are the two below and the unsaved-changes guard under Sheets.
- Android: the bottom edge (home and recents gesture) cannot be excluded at all. Side-edge exclusion via `setSystemGestureExclusionRects` is honoured for at most 200dp of vertical extent; use it only for a specific control such as a slider thumb.
- iOS 26 and later: a leading-to-trailing pan **anywhere** in a pushed screen's content can start back navigation (`interactiveContentPopGestureRecognizer`), not just at the edge. A horizontal carousel, chart scrubber, slider, or swipeable card in a pushed screen's content is allowed only with explicit conflict handling (gesture priority or `require(toFail:)` against that recognizer) and a test that both the pan and back still work.
- Carousels get visible previous and next controls. Avoid putting a carousel inside tabs that page horizontally: both gestures use the same axis, so a swipe can hit the wrong one.

## Drag to reorder

Reordering by drag also has a non-drag path: Move up and Move down actions, a Move to menu, or an Edit mode with explicit position controls. Expose the same actions to accessibility.

## Zoom

- Images, maps, and documents support both pinch and double-tap zoom, plus visible zoom in and zoom out (+/-) buttons.
- On the web, never disable browser zoom: no `user-scalable=no`, and `maximum-scale` no lower than 2 in the viewport meta tag.

## Pull to refresh

Pull to refresh also has a Refresh item in a toolbar or overflow menu, so keyboard, switch, and D-pad users can reload.

## Shake and multi-finger gestures

- Avoid them for app actions. If one is used, give it a visible tap path and a setting that turns the motion trigger off.
- Leave the system's meanings alone: on iOS, three-finger swipe and shake mean undo and redo. Do not redefine them.

## Touch targets

- Minimum hit area: 44x44pt on iOS, 48x48dp on Android. The hit area may extend past the visible glyph.
- Spacing between adjacent targets: on iOS about 12pt of padding around elements with a bezel and about 24pt around the visible edges of elements without one; on Android 8dp or more.
- Targets in screen corners are larger, about 12mm (roughly 75pt or dp). Center targets can be smaller.
- For people with upper-body motor impairments, use at least 18mm (roughly 115pt or dp); even at that size the study measured a 7% error rate.
- WCAG 2.5.8's 24x24 CSS px is a conformance minimum at Level AA, not a design target.

## Reach

Keep frequent actions reachable without strain, and make corner targets bigger. Treat the "thumb zone" heat-map as a hypothesis, not a law: observation data shows people shift grip, prefer the center of the screen, and readily reach a top-left Back button. Placing the primary action at the bottom is fine; banning actions from the top is not justified.

## Haptics

- In SwiftUI, use `sensoryFeedback(_:trigger:)` (iOS 17+), tied to a state change, rather than UIKit feedback generators.
- Play a haptic only for a meaningful outcome (success, failure, a snap into place, crossing a threshold), keep it subtle, and pair it with a visible change. Never use one as the only signal.

## Verify on a device

- Test every gesture on real hardware: simulator mouse drags hide edge conflicts, mis-taps, and reach problems.
- Run each changed flow once with VoiceOver (iOS) or TalkBack (Android) on. With a screen reader on, one-finger swipes move focus, so the app's own swipe gestures do not fire; every action must still be reachable through a visible tap path or the Actions rotor (VoiceOver) or Actions menu (TalkBack).
