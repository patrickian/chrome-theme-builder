from dataclasses import replace

from PySide6.QtCore import QObject, Signal

from ..core.settings import ThemeSettings


class AppState(QObject):
    """Holds the current settings and announces every change."""

    changed = Signal()

    def __init__(self):
        super().__init__()
        self.settings = ThemeSettings()

    def update(self, **values):
        new_settings = replace(self.settings, **values)
        if new_settings != self.settings:
            self.settings = new_settings
            self.changed.emit()
