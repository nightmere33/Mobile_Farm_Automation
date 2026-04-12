"""Locators for VFS Italy Global — align with Maestro flow.yaml where possible.

Replace or extend after Appium Inspector passes on a real device.
Use resource-id from Inspector when available; text-based selectors are brittle.
"""

# First screen country/language (Maestro: tapOn text "Algeria (English)")
# UiAutomator2: partial text match handles minor spacing differences.
COUNTRY_LANGUAGE_TEXT = "Algeria"
COUNTRY_LANGUAGE_TEXT_EXACT = "Algeria (English)"

# Optional: add resource-ids from Appium Inspector, e.g.:
# LOGIN_EMAIL_ID = "com.vfs.italyglobal:id/..."
