# Phase 1: Photo / liveness screen — findings log

Fill this in **on a real device** after you drive the flow as far as the face capture step (manually extend `automation/flows/` or use Inspector to prototype taps).

## Run metadata

| Field | Value |
|--------|--------|
| Date | |
| Device model / Android API | |
| VFS Italy Global version (if known) | |
| Appium server / uiautomator2 driver versions | |

## Observations at photo / liveness step

- **Screen type:** native / WebView / custom camera SDK (describe)
- **Can Appium see shutter / Continue controls?** yes / no / partial
- **Liveness type:** blink / head turn / passive / unknown
- **File picker or gallery path offered?** yes / no

## Automation implications

- **Pure UiAutomator2 viable?** (yes / limited / no)
- **If no:** note options you will evaluate later (e.g. pre-captured face from your intake app, operator-assisted step, policy constraints). Do not assume bypass of security controls.

## Evidence

- Attach or link screenshots: `automation/artifacts/...`
- Paste relevant **page source** snippet (redact PII)

## Face intake app (future integration)

Your separate Android liveness app produces a client photo stored on the server. For VFS, document here whether the target flow expects **live camera only**, **upload**, or **unknown** — that determines whether “injection” is a supported path or requires manual completion for that step.
