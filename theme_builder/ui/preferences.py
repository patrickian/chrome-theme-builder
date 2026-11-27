"""Choices remembered between runs (the Windows registry on Windows)."""

from PySide6.QtCore import QSettings

_SHOW_GUIDE_KEY = "show_guide_at_startup"


def _store() -> QSettings:
    return QSettings("ChromeThemeBuilder", "ChromeThemeBuilder")


def show_guide_at_startup() -> bool:
    return _store().value(_SHOW_GUIDE_KEY, True, type=bool)


def set_show_guide_at_startup(show: bool):
    _store().setValue(_SHOW_GUIDE_KEY, show)
