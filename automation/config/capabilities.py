"""Build W3C capabilities for one Android UiAutomator2 session."""

from __future__ import annotations

import os
from typing import Any


def build_capabilities() -> dict[str, Any]:
    """Load caps from environment (see config/.env.example)."""
    app_package = os.environ.get("ANDROID_APP_PACKAGE", "com.vfs.italyglobal")
    app_activity = os.environ.get("ANDROID_APP_ACTIVITY", "").strip()
    if not app_activity:
        raise RuntimeError(
            "ANDROID_APP_ACTIVITY is not set. "
            "Install VFS Italy Global on the device, then run:\n"
            "  adb shell cmd package resolve-activity --brief "
            f"{app_package}\n"
            "and set ANDROID_APP_ACTIVITY in automation/.env to the launcher activity."
        )

    udid = os.environ.get("ANDROID_UDID", "").strip()
    caps: dict[str, Any] = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": app_package,
        "appium:appActivity": app_activity,
        "appium:noReset": os.environ.get("ANDROID_NO_RESET", "false").lower()
        in ("1", "true", "yes"),
        "appium:newCommandTimeout": 300,
        "appium:uiautomator2ServerLaunchTimeout": 120_000,
    }
    if udid:
        caps["appium:udid"] = udid
    return caps
