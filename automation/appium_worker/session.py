"""Create and quit an Appium driver for the POC."""

from __future__ import annotations

import os

from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver

from automation.config.capabilities import build_capabilities


def create_driver() -> WebDriver:
    url = os.environ.get("APPIUM_SERVER_URL", "http://127.0.0.1:4723").rstrip("/")
    caps = build_capabilities()
    options = UiAutomator2Options().load_capabilities(caps)
    return WebDriver(f"{url}/", options=options)


def implicit_wait(driver, seconds: float | None = None) -> None:
    if seconds is None:
        seconds = float(os.environ.get("IMPLICIT_WAIT_SECONDS", "15"))
    driver.implicitly_wait(seconds)
