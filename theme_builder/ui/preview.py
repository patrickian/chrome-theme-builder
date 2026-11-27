import os

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QColor, QImage, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ..core.assets import DEFAULT_ICON
from ..media.images import cover_source_rect, load_icon
from ..media.video import VideoPlayer
from . import theme
from .draw_chrome import CHROME_H, draw_chrome
from .draw_shortcuts import draw_shortcuts
from .paint_utils import draw_text
from .state import AppState

# The mock browser is drawn at this size (16:9) and scaled to fit the widget.
DESIGN_W = 1280
DESIGN_H = 720


class PreviewWidget(QWidget):
    """A landscape mock browser window showing the theme and new tab page."""

    def __init__(self, state: AppState, video: VideoPlayer):
        super().__init__()
        self.state = state
        self.video = video
        self.icon: QImage | None = None
        self._default_icon = load_icon(str(DEFAULT_ICON))

        self.setMinimumSize(480, 270)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        state.changed.connect(self.update)
        video.frame_changed.connect(self.update)

    def sizeHint(self) -> QSize:
        return QSize(960, 540)

    def set_icon(self, icon: QImage | None):
        self.icon = icon
        self.update()

    def window_rect(self) -> QRectF:
        """The largest 16:9 area, centered horizontally and resting on the bottom."""
        scale = min(self.width() / DESIGN_W, (self.height() - 1) / DESIGN_H)
        rect = QRectF(0, 0, DESIGN_W * scale, DESIGN_H * scale)
        rect.moveLeft((self.width() - rect.width()) / 2)
        rect.moveBottom(self.height() - 1)
        return rect

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHints(
            QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform
        )

        target = self.window_rect()
        p.translate(target.topLeft())
        p.scale(target.width() / DESIGN_W, target.height() / DESIGN_H)

        window = QRectF(0, 0, DESIGN_W, DESIGN_H)
        outline = QPainterPath()
        outline.addRoundedRect(window, 14, 14)

        p.save()
        p.setClipPath(outline)
        page = QRectF(0, CHROME_H, DESIGN_W, DESIGN_H - CHROME_H)
        self._draw_page(p, page)
        icon = self.icon if self.icon is not None else self._default_icon
        draw_chrome(p, DESIGN_W, self.state.settings, icon)
        draw_shortcuts(p, page, self.state.settings)
        p.restore()

        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(theme.BORDER), 2))
        p.drawPath(outline)

    def _draw_page(self, p: QPainter, page: QRectF):
        """The video background, or a placeholder until one is playing."""
        frame = self.video.frame
        if frame is not None:
            p.fillRect(page, QColor("black"))
            p.drawImage(page, frame, cover_source_rect(frame.size(), page.size()))
            return

        gradient = QLinearGradient(page.topLeft(), page.bottomRight())
        gradient.setColorAt(0, QColor("#273449"))
        gradient.setColorAt(1, QColor("#121826"))
        p.fillRect(page, gradient)

        path = self.state.settings.video_path
        if path and not VideoPlayer.is_available():
            message = "Install 'opencv-python' to play the video preview"
        elif path:
            message = f"Selected: {os.path.basename(path)}"
        else:
            message = "Select an .mp4 video to preview the background"
        draw_text(
            p, QRectF(0, page.bottom() - 56, DESIGN_W, 30), message, QColor("#94a3b8"), 16,
            align=Qt.AlignHCenter,
        )
