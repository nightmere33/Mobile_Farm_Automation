"""First steps after app launch (parity with Maestro flow.yaml)."""

from __future__ import annotations

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from automation.selectors import vfs_italy_global as sel


def tap_country_language(driver: WebDriver, timeout: float = 30.0) -> None:
    """Tap the country/language row matching Maestro `Algeria (English)`."""
    wait = WebDriverWait(driver, timeout)
    # Prefer exact-ish text; fall back to partial match.
    strategies = [
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{sel.COUNTRY_LANGUAGE_TEXT_EXACT}")'),
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{sel.COUNTRY_LANGUAGE_TEXT}")',
        ),
    ]
    last: Exception | None = None
    for by, value in strategies:
        try:
            el = wait.until(EC.element_to_be_clickable((by, value)))
            el.click()
            return
        except TimeoutException as exc:
            last = exc
            continue
    raise TimeoutException(
        "Could not tap country/language. Update selectors in "
        "automation/selectors/vfs_italy_global.py after Appium Inspector."
    ) from last


def type_first_edittext_if_present(driver: WebDriver, text: str, timeout: float = 8.0) -> bool:
    """POC helper: first visible EditText. Returns True if typing was attempted."""
    if not text.strip():
        return False
    wait = WebDriverWait(driver, timeout)
    locator = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").focused(true)',
    )
    try:
        el = wait.until(EC.presence_of_element_located(locator))
    except TimeoutException:
        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(0)',
        )
        try:
            el = wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return False
    el.click()
    el.clear()
    el.send_keys(text)
    return True
