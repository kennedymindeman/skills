---
name: app-release
description: Versions and distributes iOS and Android app builds. Use when starting a TestFlight or Firebase build, uploading a build, bumping an app's version or build number, creating an external TestFlight group, sending a build to testers, or quoting how long a build will take.
---

# App release

## Versions

Each app has one semver version shared by iOS and Android, `major.minor.patch`. Every upload bumps it, retries included.

- The store build number is derived from it: major × 10000 + minor × 100 + patch. The version is the only number anyone manages.
- Upload scripts parse the version with a semver library and refuse a version not higher than the last upload.
- Before a public launch the major is 0.
- Bump minor when testers can do something new (a new screen, control, or workout type).
- Bump patch for fixes, for changes to how existing things behave or look, and for retries.
- Bump major for a breaking data change or, from 0 to 1, the public launch.
- The app shows the version where testers can read it, and feedback reports attach it.

## Distribution

- Send each build to the owner's own devices (the internal TestFlight group) as it lands.
- Send builds to outside testers (external TestFlight groups, Firebase) only when the owner says, batched, so they aren't updated every day.
- When a new external TestFlight group is created, submit the latest known-good build for beta review right away. Creating the group counts as the owner's go-ahead for its first build.
- Quote build waits from measured past runs, never estimates.

## Build notifications

Run a TestFlight build in the background. When it exits, send one push notification: the app, the commit, and whether it uploaded or failed, with the log path on failure. Send nothing when Apple finishes processing; App Store Connect already emails that.
