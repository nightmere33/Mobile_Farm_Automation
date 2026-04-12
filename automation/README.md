# Phase 1: Appium worker (one device)

## Prerequisites (this machine)

- **Node.js** — Appium CLI
- **Appium 2** — `npm i -g appium`
- **UiAutomator2 driver for Appium 2.x** — default `appium driver install uiautomator2` targets Appium 3; use:

  ```text
  appium driver install uiautomator2@2
  ```

- **Java JDK 17+** — required by UiAutomator2 / Android tooling
- **Android platform-tools** — `adb` on `PATH`
- **Optional:** full Android SDK with `ANDROID_HOME` set (helps some driver features; not always mandatory for USB device + installed app)

## Appium Inspector

Download the desktop build from the [Appium Inspector releases](https://github.com/appium/appium-inspector/releases).

**Remote path:** `http://127.0.0.1:4723/` (default Appium 2 base path).

**Capabilities:** use the JSON template in [docs/selectors-from-inspector.md](../docs/selectors-from-inspector.md) and set `appium:appActivity` after you resolve it on a device (below).

## Device: `udid` and launcher activity

1. USB debugging on; connect the phone; authorize the PC.

   ```powershell
   adb devices -l
   ```

   If multiple devices appear, set `ANDROID_UDID` in `automation/.env` to the serial shown.

2. Install **VFS Italy Global** on the device (`com.vfs.italyglobal`).

3. Resolve the launcher activity (adjust package if your build differs):

   ```powershell
   adb shell cmd package resolve-activity --brief com.vfs.italyglobal
   ```

   Set `ANDROID_APP_ACTIVITY` in `automation/.env` to the activity component after the `/` (often something like `com.vfs.italyglobal/.SomeActivity` — use the part after `/` with leading dot expanded to full class name if needed).

## Configure and run

1. Copy [config/.env.example](config/.env.example) to `automation/.env` at repo root path `vfs-automation/automation/.env`.

2. Create a venv and install Python deps from repo root:

   ```powershell
   cd c:\automation\mobile_farm\vfs-automation
   python -m venv .venv
   .\.venv\Scripts\pip install -r automation\requirements.txt
   ```

3. Start Appium in a separate terminal:

   ```powershell
   appium
   ```

4. Run the POC:

   ```powershell
   .\.venv\Scripts\python -m automation.appium_worker.run_poc
   ```

The script starts a session, launches the app via `appPackage` / `appActivity`, then taps the country/language row matching [flow.yaml](../flow.yaml) (Algeria / English). On failure it saves `automation/artifacts/poc_failure.png` if possible.

## Next steps

- Capture stable **resource-id** selectors in Appium Inspector; paste into `automation/selectors/vfs_italy_global.py`.
- Extend `automation/flows/` for later booking steps; document photo/liveness in [docs/phase1-liveness-notes.md](../docs/phase1-liveness-notes.md).
