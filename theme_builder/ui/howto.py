"""The Guide/Manual window: what to do with the generated ZIP."""

import html
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..core.settings import DEFAULT_ZIP_NAME, PACKAGE_NAME
from . import preferences
from .widgets import Card, make_label

EXTENSIONS_URL = "chrome://extensions"

# (title, instructions) for each step; instructions may use simple HTML.
STEPS = [
    (
        "Extract the ZIP",
        f"Right-click <b>{DEFAULT_ZIP_NAME}</b> and choose <b>Extract All</b>. Put the folder somewhere "
        "permanent: Chrome keeps loading the files from there, so don't move or delete it afterwards.",
    ),
    (
        "Open Chrome's extensions page",
        f"Type <b>{EXTENSIONS_URL}</b> in Chrome's address bar and press Enter, "
        "then turn on <b>Developer mode</b> (top right).",
    ),
    (
        "Load the new tab page",
        f"Click <b>Load unpacked</b> and select the <b>{PACKAGE_NAME}/video-tab</b> folder.",
    ),
    (
        "Load the theme",
        f"Click <b>Load unpacked</b> again and select the <b>{PACKAGE_NAME}/my-theme</b> folder. "
        "It applies right away and colors the tabs and toolbar.",
    ),
    (
        "Open a new tab",
        "If Chrome asks whether to keep the new page, choose to keep it. "
        "Use <b>+ Add Shortcut</b> to add your sites.",
    ),
]

NOTES = [
    (
        "Updating later",
        "Generate a new ZIP and extract it over the same folder, then click the reload icon on "
        "<b>My Video Tab</b> and load <b>my-theme</b> again. Keeping the same folder keeps your shortcuts.",
    ),
    (
        "Removing it",
        "Remove <b>My Video Tab</b> on the extensions page (this also deletes its shortcuts). "
        "To restore Chrome's colors, open <b>Settings &gt; Appearance</b> and reset the theme.",
    ),
]


class HowToDialog(QDialog):
    """Install steps. Pass `saved_zip` right after generating to show where it went."""

    def __init__(self, parent=None, saved_zip: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Success" if saved_zip else "Guide/Manual")
        self.resize(560, 620)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 16)
        layout.setSpacing(10)

        layout.addWidget(make_label("How to install your theme", "appTitle"))
        if saved_zip:
            saved = make_label(f"Saved to {saved_zip}", "muted")
            saved.setTextFormat(Qt.PlainText)
            saved.setWordWrap(True)
            saved.setTextInteractionFlags(Qt.TextSelectableByMouse)
            layout.addWidget(saved)

        layout.addWidget(self._build_steps(), 1)
        layout.addWidget(self._build_startup_checkbox())
        layout.addLayout(self._build_buttons(saved_zip))

    @staticmethod
    def _build_steps() -> QScrollArea:
        body = QWidget()
        column = QVBoxLayout(body)
        column.setContentsMargins(0, 0, 6, 0)
        column.setSpacing(8)

        numbered = [(f"{number}. {title}", text) for number, (title, text) in enumerate(STEPS, 1)]
        for title, text in numbered + NOTES:
            card = Card()
            card.body.addWidget(make_label(f"<b>{html.escape(title)}</b>"))
            details = make_label(text, "muted")
            details.setWordWrap(True)
            details.setTextInteractionFlags(Qt.TextSelectableByMouse)
            card.body.addWidget(details)
            column.addWidget(card)
        column.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(body)
        return scroll

    @staticmethod
    def _build_startup_checkbox() -> QCheckBox:
        """Unticking it later brings the guide back at startup."""
        checkbox = QCheckBox("Don't show this guide at startup")
        checkbox.setChecked(not preferences.show_guide_at_startup())
        checkbox.toggled.connect(lambda hide: preferences.set_show_guide_at_startup(not hide))
        return checkbox

    def _build_buttons(self, saved_zip: str) -> QHBoxLayout:
        row = QHBoxLayout()

        # Other programs cannot open chrome:// pages, so offer the address to paste.
        copy_btn = QPushButton(f"Copy {EXTENSIONS_URL}")

        def copy_address():
            QGuiApplication.clipboard().setText(EXTENSIONS_URL)
            copy_btn.setText("Copied")

        copy_btn.clicked.connect(copy_address)
        row.addWidget(copy_btn)

        if saved_zip:
            folder_btn = QPushButton("Open ZIP folder")
            folder = str(Path(saved_zip).parent)
            folder_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(folder)))
            row.addWidget(folder_btn)

        row.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.accept)
        row.addWidget(close_btn)
        return row
