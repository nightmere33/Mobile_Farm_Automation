"""Phase 1 POC: start session, open VFS Italy Global, first tap (Maestro parity).

Run from repo root (vfs-automation):

  1. Start Appium: appium
  2. Connect one device; set ANDROID_APP_ACTIVITY in automation/.env
  3.  python -m automation.appium_worker.run_poc
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from automation.appium_worker.session import create_driver, implicit_wait
from automation.flows import bootstrap

_LOG = logging.getLogger(__name__)


def _load_env() -> None:
    repo = Path(__file__).resolve().parents[2]
    env_path = repo / "automation" / ".env"
    load_dotenv(env_path)
    if not env_path.is_file():
        _LOG.warning("Missing %s; copy automation/config/.env.example to automation/.env", env_path)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    _load_env()
    driver = None
    try:
        driver = create_driver()
        implicit_wait(driver)
        _LOG.info("Session started; running bootstrap flow")
        bootstrap.tap_country_language(driver)
        _LOG.info("Bootstrap tap completed")
        sample = os.environ.get("POC_SAMPLE_TEXT", "").strip()
        if sample:
            if bootstrap.type_first_edittext_if_present(driver, sample):
                _LOG.info("POC_SAMPLE_TEXT sent to first EditText")
            else:
                _LOG.warning("POC_SAMPLE_TEXT set but no EditText found; extend flows after Inspector")
        return 0
    except Exception:
        _LOG.exception("POC failed")
        if driver is not None:
            try:
                shot = Path(__file__).resolve().parents[2] / "automation" / "artifacts" / "poc_failure.png"
                shot.parent.mkdir(parents=True, exist_ok=True)
                driver.save_screenshot(str(shot))
                _LOG.info("Screenshot: %s", shot)
            except Exception:
                _LOG.exception("Could not save screenshot")
        return 1
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    sys.exit(main())
