"""The logo and contact address at the bottom of the sidebar."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..core.assets import BRAND_LOGO
from . import theme
from .widgets import make_label

CONTACT_EMAIL = "dundernomads@gmail.com"
LOGO_SIZE = 28


class BrandFooter(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        logo = make_label("")
        logo.setPixmap(self._logo_pixmap())
        layout.addWidget(logo)

        texts = QVBoxLayout()
        texts.setSpacing(0)
        texts.addStretch(1)
        texts.addWidget(make_label("Contact us", "muted"))

        # Clicking opens the default mail program; the text can also be selected.
        email = make_label(
            f'<a href="mailto:{CONTACT_EMAIL}" style="color: {theme.ACCENT}; text-decoration: none;">'
            f"{CONTACT_EMAIL}</a>"
        )
        email.setOpenExternalLinks(True)
        email.setTextInteractionFlags(Qt.TextBrowserInteraction)
        texts.addWidget(email)
        texts.addStretch(1)
        layout.addLayout(texts, 1)

    def _logo_pixmap(self) -> QPixmap:
        """Scale for the screen's pixel density so the logo stays sharp."""
        ratio = self.devicePixelRatioF()
        pixels = round(LOGO_SIZE * ratio)
        pixmap = QPixmap(str(BRAND_LOGO)).scaled(
            pixels, pixels, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        pixmap.setDevicePixelRatio(ratio)
        return pixmap
