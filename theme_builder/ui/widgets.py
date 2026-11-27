"""Small reusable controls for the sidebar."""

import os

from PySide6.QtCore import QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFontMetrics, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QColorDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

SWATCH = 14  # size of the color square, in pixels


def make_divider() -> QFrame:
    """A one pixel horizontal line."""
    divider = QFrame()
    divider.setObjectName("divider")
    divider.setFixedHeight(1)
    return divider


def make_swatch(color: str, ratio: float) -> QIcon:
    """A small rounded square filled with `color`."""
    pixmap = QPixmap(round(SWATCH * ratio), round(SWATCH * ratio))
    pixmap.setDevicePixelRatio(ratio)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(color))
    # A light edge keeps dark colors visible on the dark sidebar.
    painter.setPen(QColor(255, 255, 255, 70))
    painter.drawRoundedRect(QRectF(0.5, 0.5, SWATCH - 1, SWATCH - 1), 3, 3)
    painter.end()
    return QIcon(pixmap)


def make_label(text: str, style_name: str = "") -> QLabel:
    label = QLabel(text)
    label.setObjectName(style_name)
    return label


class Card(QFrame):
    """A rounded box; add rows to `self.body`."""

    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(14, 14, 14, 14)
        self.body.setSpacing(8)


class FileRow(QWidget):
    """A title, the chosen file's name and a Browse button."""

    browse_requested = Signal()

    def __init__(self, title: str, empty_text: str):
        super().__init__()
        self._empty_text = empty_text

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        texts = QVBoxLayout()
        texts.setSpacing(0)
        texts.addWidget(make_label(title))
        self._name = make_label(empty_text, "muted")
        # Long names are elided in set_path instead of widening the sidebar.
        self._name.setMinimumWidth(1)
        texts.addWidget(self._name)
        layout.addLayout(texts, 1)

        button = QPushButton("Browse...")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.browse_requested)
        layout.addWidget(button)

    def set_path(self, path: str):
        name = os.path.basename(path) if path else self._empty_text
        metrics = QFontMetrics(self._name.font())
        self._name.setText(metrics.elidedText(name, Qt.ElideMiddle, 180))
        self._name.setToolTip(path)


class ColorRow(QWidget):
    """A title and a button showing the color, which opens the color picker."""

    color_picked = Signal(str)

    def __init__(self, title: str, color: str):
        super().__init__()
        self._title = title

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(make_label(title), 1)

        self._button = QPushButton()
        self._button.setObjectName("swatch")
        self._button.setFixedWidth(92)
        self._button.setIconSize(QSize(SWATCH, SWATCH))
        self._button.setCursor(Qt.PointingHandCursor)
        self._button.setToolTip("Pick color")
        self._button.clicked.connect(self._pick)
        layout.addWidget(self._button)

        self.set_color(color)

    def set_color(self, color: str):
        self._color = color
        self._button.setIcon(make_swatch(color, self.devicePixelRatioF()))
        self._button.setText(color.upper())

    def _pick(self):
        chosen = QColorDialog.getColor(QColor(self._color), self.window(), self._title)
        if chosen.isValid():
            self.set_color(chosen.name())
            self.color_picked.emit(chosen.name())
