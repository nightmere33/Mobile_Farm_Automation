# Appium Inspector: capabilities and selectors

Use this after `appium` is running and one device is connected.

## Desired capabilities (template)

Paste into Appium Inspector (JSON representation). Replace `appActivity` and optionally `udid` with values from your device.

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:appPackage": "com.vfs.italyglobal",
  "appium:appActivity": "YOUR_LAUNCHER_ACTIVITY_HERE",
  "appium:noReset": false,
  "appium:newCommandTimeout": 300
}
```

If you use a single device and omit `udid`, Appium uses the only connected device.

## What to record for Phase 1

For the first three screens after launch:

1. Whether elements are **native** (`android.widget.*`) or inside a **WebView** (Context switch may be required: `driver.contexts`).
2. Prefer **resource-id** (`appium:id/...`) over XPath when stable.
3. For list rows, note **text**, **content-desc**, and **clickable parent** bounds.

Update [automation/selectors/vfs_italy_global.py](../automation/selectors/vfs_italy_global.py) with the ids you find; keep text-based fallbacks only where ids are missing.

## Hybrid apps

If the hierarchy shows `WEBVIEW_...`:

- You may need `chromedriverExecutableDir` or matching ChromeDriver for the system WebView version (document the exact error if you hit a driver mismatch).

Record that in [phase1-liveness-notes.md](phase1-liveness-notes.md) when you reach the photo step.
