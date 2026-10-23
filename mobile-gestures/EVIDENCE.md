# Evidence behind mobile-gestures

Each section of `SKILL.md` maps to the sources below. Quotes are from the linked pages.

## Every gesture is a shortcut

- [Apple HIG: Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures): a custom gesture must be "not the only way to perform an important action"; "Use shortcut gestures to supplement standard gestures, not replace them."
- [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility): "if you use a swipe gesture to dismiss a view, also make a button available so people can tap or use an assistive device."
- [WCAG 2.2 SC 2.5.1 Pointer Gestures](https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html): multipoint and path-based gestures must also work with a single pointer without a path.
- [SwiftUI `accessibilityAction(named:_:)`](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:)): adds a named action that VoiceOver and other assistive technologies can invoke.
- [Compose semantics: custom actions](https://developer.android.com/develop/ui/compose/accessibility/semantics): the swipe-to-dismiss example exposes the swipe as `customActions = listOf(CustomAccessibilityAction(label = "Remove article from list", ...))`.
- [NN/g: Contextual Swipe](https://www.nngroup.com/articles/contextual-swipe/): swipe has no signifiers, so actions behind it are found by accident or not at all.
- [WCAG 2.2 SC 2.5.7 Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html): drag needs a single-pointer alternative.
- Apple's HIG lists swipe, pinch, long press, and drag as standard gestures. This skill still treats them as shortcuts because they lack visible signifiers (NN/g) and WCAG requires single-pointer alternatives for path and multipoint gestures. No study shows that long press or double tap specifically go unfound; the twin rule for them rests on the signifier argument.
- [UIKit `accessibilityCustomActions`](https://developer.apple.com/documentation/objectivec/nsobject-swift.class/accessibilitycustomactions) and [AndroidX `ViewCompat.addAccessibilityAction`](https://developer.android.com/reference/androidx/core/view/ViewCompat#addAccessibilityAction(android.view.View,java.lang.CharSequence,androidx.core.view.accessibility.AccessibilityViewCommand)): the UIKit and Android Views equivalents of the SwiftUI and Compose APIs.

## Row swipe

- [NN/g: Contextual Swipe](https://www.nngroup.com/articles/contextual-swipe/): "Limit contextual swipe to destructive actions"; users expect Delete and Remove there, and nonstandard actions (Spotify's save-a-song) go unexpected.
- [Android: Swipe to dismiss or update (Compose, Material 3 `SwipeToDismissBox`)](https://developer.android.com/develop/ui/compose/touch-input/user-interactions/swipe-to-dismiss): Google's sample puts a non-destructive "mark as complete" on one swipe direction and Delete on the other. This is the disagreement with NN/g that `SKILL.md` resolves by mirroring.
- [SwiftUI `swipeActions(edge:allowsFullSwipe:content:)`](https://developer.apple.com/documentation/swiftui/view/swipeactions(edge:allowsfullswipe:content:)): `allowsFullSwipe` "indicates whether a full swipe automatically performs the first action. The default is true."

## Destructive actions: undo first, confirm rarely

- [Apple HIG: Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts): "Avoid displaying alerts for common, undoable actions, even when they're destructive"; for "an uncommon destructive action that they can't undo, it's important to display an alert."
- [NN/g: Contextual Swipe](https://www.nngroup.com/articles/contextual-swipe/): where confirming a frequent action is tedious, "support easy undo" with the undo clearly visible.
- [Material 3: Snackbar accessibility](https://m3.material.io/components/snackbar/accessibility): snackbars with an action should not auto-dismiss, so screen-reader users can reach the action. The page renders client-side; the rule is corroborated by [Flutter's breaking change "SnackBar with action no longer auto-dismisses"](https://docs.flutter.dev/release/breaking-changes/snackbar-with-action-behavior-update), which "aligns with the Material 3 design specification" and "improves accessibility", and by [Angular Material's snack-bar accessibility notes](https://v10.material.angular.io/components/snack-bar/overview), which advise against a duration on snackbars with an action.

## Sheets

- [NN/g: Bottom Sheets](https://www.nngroup.com/articles/bottom-sheet/): the grab handle "is easy to ignore"; "We recommend providing a clear Close button ... rather than relying exclusively on the grab handle."
- [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility): swipe-to-dismiss needs a button too (quoted above).
- [Apple HIG: Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets): Cancel (or Close) dismisses without saving; Done dismisses after completing or saving.
- [Android: Predictive back design](https://developer.android.com/design/ui/mobile/guides/patterns/predictive-back): bottom sheets and side sheets take part in the system back gesture and its animation.
- [SwiftUI `interactiveDismissDisabled(_:)`](https://developer.apple.com/documentation/swiftui/view/interactivedismissdisabled(_:)): "prevent nonprogrammatic dismissal of the containing view hierarchy when presented in a sheet or popover." It blocks the swipe and offers no callback when someone attempts it.
- [UIKit `presentationControllerDidAttemptToDismiss(_:)`](https://developer.apple.com/documentation/uikit/uiadaptivepresentationcontrollerdelegate/presentationcontrollerdidattempttodismiss(_:)): called when a dismissal is prevented (for example by `isModalInPresentation`), which is where a confirm-on-swipe dialog goes.
- [Android: Add support for the predictive back gesture](https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture): "The \"Are you sure...\" PredictiveBackHandler is enabled when the user enters data into a form, and disabled otherwise. When enabled, it intercepts the back gesture to display a confirmation dialog."
- No source found that frames the unsaved-changes guard itself as guidance; the Apple HIG Sheets page does not cover it. It follows from the undo-or-confirm rule above: closing a dirty form loses data that cannot be recovered.

## System gestures own the edges

- [Android: Gesture navigation](https://developer.android.com/develop/ui/views/touch-and-input/gestures/gesturenav): for home and quick switch at the bottom, "Apps can't opt out of these gestures as they can with the back gesture."
- [Android `View.setSystemGestureExclusionRects`](https://developer.android.com/reference/android/view/View#setSystemGestureExclusionRects(java.util.List%3Candroid.graphics.Rect%3E)): "the system will put a limit of 200dp on the vertical extent of the exclusions it takes into account." The limit does not apply while the navigation bar is stickily hidden.
- [Android: Predictive back design](https://developer.android.com/design/ui/mobile/guides/patterns/predictive-back): "Avoid adding touch gestures or drag targets under these gesture areas."
- [Android 16 behavior changes](https://developer.android.com/about/versions/16/behavior-changes-16): for apps targeting API 36, predictive back animations are on by default and `onBackPressed` is not called.
- [Android: Add support for the predictive back gesture](https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture): an enabled back callback suppresses the predictive animation; "Don't create these callbacks to run business logic or to log."
- [UIKit `interactiveContentPopGestureRecognizer`](https://developer.apple.com/documentation/uikit/uinavigationcontroller/interactivecontentpopgesturerecognizer) (iOS 26.0+): pops the top view controller "when a person initially pans horizontally in a leading to trailing direction" and "recognizes a gesture on the entire content area"; "Use this property to retrieve the gesture recognizer and tie it to the behavior of other gesture recognizers."
- [W3C WAI Carousels tutorial: Functionality](https://www.w3.org/WAI/tutorials/carousels/functionality/): "Add previous and next buttons."
- [Android: Swipe views](https://developer.android.com/guide/navigation/navigation-swipe-view-2): tabs commonly page with "a horizontal finger gesture", the same axis a carousel uses. The rule against nesting them is an inference from that shared axis, not a quoted guideline.

## Drag to reorder

- [WCAG 2.2 SC 2.5.7 Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html): "All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging."

## Zoom

- [WCAG 2.2 SC 2.5.1 Pointer Gestures](https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html): pinch is multipoint, so zoom needs single-pointer controls (+/- buttons).
- [Apple HIG: Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures): "Support standard gestures everywhere you can"; pinch zooms.
- [Deque axe rule `meta-viewport`](https://dequeuniversity.com/rules/axe/4.10/meta-viewport) (WCAG 1.4.4): "Remove the user-scalable="no" parameter ... and ensure the maximum-scale parameter is not less than 2."

## Pull to refresh

- [Android: Add swipe-to-refresh](https://developer.android.com/develop/ui/views/touch-and-input/swipe/add-swipe-interface): "Add a refresh action to your app's action bar so users who can't perform swipe gestures can trigger a manual update", as an overflow menu item.

## Shake and multi-finger gestures

- [WCAG 2.2 SC 2.5.4 Motion Actuation](https://www.w3.org/WAI/WCAG22/Understanding/motion-actuation.html): motion-triggered functions "can also be operated by user interface components and responding to the motion can be disabled."
- [Apple HIG: Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures): three-finger swipe means undo and redo; shake means undo and redo.
- [Apple HIG: Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo): "people can use a three-finger swipe to initiate an undo or redo, or shake their iPhone."

## Touch targets

- [Apple HIG: Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons): "a button needs a hit region of at least 44x44 pt."
- [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility): iOS default control size 44x44pt; "Include enough padding between elements to reduce the chance that someone taps the wrong control. In general, it works well to add about 12 points of padding around elements that include a bezel. For elements without a bezel, about 24 points of padding works well around the element's visible edges."
- [Android Accessibility Help: Touch target size](https://support.google.com/accessibility/android/answer/7101858): touch targets at least 48x48dp, separated by 8dp or more.
- [Android: Make apps more accessible](https://developer.android.com/guide/topics/ui/accessibility/apps): "each interactive UI element have a focusable area, or touch target size, of at least 48dpx48dp."
- [Hoober 2017, Design for Fingers, Touch, and People, Part 1](https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php): center targets can be "as small as 7 millimeters, while corner target sizes must be about 12 millimeters."
- [Findlater et al., CHI 2017, Comparing Touchscreen and Mouse Input Performance by People With and Without Upper Body Motor Impairments](https://makeabilitylab.cs.washington.edu/media/publications/Findlater_ComparingTouchscreenAndMouseInputPerformanceByPeopleWithAndWithoutUpperBodyMotorImpairments_CHI2017.pdf): updates minimum touchscreen target recommendations for people with upper-body motor impairments to at least 18mm; the error rate at 18mm was still 7%. The study did not cover older adults as a group.
- [WCAG 2.2 SC 2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html): 24x24 CSS px at Level AA, described as "a minimum size". The Level AAA criterion 2.5.5 asks for 44x44.

## Reach

- [Hoober 2017](https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php): "The well-known, but incorrect thumb-sweep chart"; people "prefer to view and touch the center of the screen."

## Haptics

- [SwiftUI `sensoryFeedback(_:trigger:)`](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:)): "Plays the specified feedback when the provided trigger value changes."
- [Apple HIG: Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics): "Prefer using haptics to complement other feedback"; "Avoid overusing haptics."

## Verify on a device

- [Apple HIG: Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures): "make sure to test your interactions in real use scenarios"; "Continually test ergonomics of all interactions that require custom gestures."
- [Apple Support: Learn VoiceOver gestures on iPhone](https://support.apple.com/guide/iphone/learn-voiceover-gestures-iph3e2e2281/ios): with VoiceOver on, swipe right and left select the next and previous item.
- [Android Accessibility Help: TalkBack gestures](https://support.google.com/accessibility/android/answer/6151827): swipe right and left move to the next and previous item.

## Unverified

- Whether SwiftUI `swipeActions` and UIKit table-view swipe actions appear automatically in VoiceOver's Actions rotor. Apple's documentation does not say; only third-party posts claim it. Test it with VoiceOver on, and add `accessibilityAction(named:_:)` if the action is missing.
- No usage data was found on how many users discover pull to refresh or shake. Most NN/g gesture guidance is expert review, not a reported study.
