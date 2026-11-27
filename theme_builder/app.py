import ctypes
import sys

import shiboken6
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .builder import ExtensionPackageBuilder
from .core.assets import DEFAULT_ICON
from .core.settings import DEFAULT_ZIP_NAME
from .media.images import load_icon
from .media.video import VideoPlayer
from .ui import preferences
from .ui.controls import ControlsPanel
from .ui.howto import HowToDialog
from .ui.preview import DESIGN_H, DESIGN_W, PreviewWidget
from .ui.state import AppState
from .ui.theme import apply_theme
from .ui.widgets import make_label


# Spacing around the preview, in pixels
STAGE_EDGE = 12
STAGE_GAP = 8


class MainWindow(QMainWindow):
    """Connects the controls, the preview, video playback and the builder."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chrome Video Tab & Theme Builder")
        self.state = AppState()
        self.video = VideoPlayer()

        self.controls = ControlsPanel(self.state)
        self.controls.pick_video_requested.connect(self._pick_video)
        self.controls.pick_icon_requested.connect(self._pick_icon)
        self.controls.generate_requested.connect(self._generate_zip)
        self.preview = PreviewWidget(self.state, self.video)

        root = QWidget()
        root.setObjectName("root")
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.controls)

        header = self._build_preview_header()
        # The preview ends level with the line above the sidebar's contact area.
        # (It keeps one pixel below itself so its outline is not clipped.)
        self.ensurePolished()
        bottom = self.controls.footer_line_offset() - 1
        stage = QVBoxLayout()
        stage.setContentsMargins(STAGE_EDGE, STAGE_EDGE, STAGE_EDGE, bottom)
        stage.setSpacing(STAGE_GAP)
        stage.addLayout(header)
        stage.addWidget(self.preview, 1)
        layout.addLayout(stage, 1)
        self.setCentralWidget(root)

        self._fit_to_content(header.sizeHint().height(), bottom)

    def _fit_to_content(self, header_height: int, bottom: int):
        """Open at the size where the sidebar and the 16:9 preview both fit snugly."""
        height = self.controls.content_height()
        preview_height = height - header_height - STAGE_GAP - STAGE_EDGE - bottom - 1
        width = self.controls.width() + 2 * STAGE_EDGE + round(preview_height * DESIGN_W / DESIGN_H)

        # Never larger than the screen.
        screen = self.screen().availableGeometry()
        max_height = screen.height() - 40  # leave room for the title bar
        self.setMinimumSize(min(960, screen.width()), min(height, max_height))
        self.resize(min(width, screen.width()), min(height, max_height))

    def _build_preview_header(self) -> QHBoxLayout:
        titles = QVBoxLayout()
        titles.setSpacing(0)
        titles.addWidget(make_label("Live preview", "pageTitle"))
        titles.addWidget(make_label("How your browser will look with these settings", "muted"))

        how_to = QPushButton("Guide/Manual")
        how_to.setObjectName("highlight")
        how_to.setCursor(Qt.PointingHandCursor)
        how_to.setToolTip("What to do after generating the ZIP")
        how_to.clicked.connect(lambda: self._show_how_to())

        header = QHBoxLayout()
        header.addLayout(titles, 1)
        header.addWidget(how_to)
        return header

    def _show_how_to(self, saved_zip: str = ""):
        HowToDialog(self, saved_zip).exec()

    def show_startup_guide(self):
        if preferences.show_guide_at_startup():
            self._show_how_to()

    def closeEvent(self, event):
        self.video.stop()
        super().closeEvent(event)

    def _pick_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Background Video", "", "MP4 Video (*.mp4);;All Files (*)"
        )
        if not path:
            return
        self.state.update(video_path=path)
        self.video.start(path)

    def _pick_icon(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Tab Icon", "", "Image Files (*.png *.ico *.jpg *.jpeg *.webp);;All Files (*)"
        )
        if not path:
            return
        self.state.update(icon_path=path)
        self.preview.set_icon(load_icon(path))

    def _generate_zip(self):
        if not self.state.settings.video_path:
            QMessageBox.critical(self, "Missing Video", "Please select an .mp4 video file first.")
            return

        dialog = QFileDialog(self, "Save Extension Package", "", "ZIP Archive (*.zip)")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("zip")
        dialog.selectFile(DEFAULT_ZIP_NAME)
        if not dialog.exec():
            return
        save_zip_path = dialog.selectedFiles()[0]

        try:
            ExtensionPackageBuilder(self.state.settings).build(save_zip_path)
        except Exception as exc:
            QMessageBox.critical(self, "Build Failed", str(exc))
            return
        self._show_how_to(save_zip_path)


def _use_own_taskbar_icon():
    """Stop Windows from grouping the app under Python's taskbar icon."""
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ChromeThemeBuilder")


def main():
    _use_own_taskbar_icon()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(DEFAULT_ICON)))
    apply_theme(app)
    window = MainWindow()
    window.show()
    # Open the guide once the event loop runs, so the main window is behind it.
    QTimer.singleShot(0, window.show_startup_guide)
    exit_code = app.exec()
    # Destroy the window while Qt is still running. Left to Python's shutdown,
    # it can be freed after the application object, which crashes.
    shiboken6.delete(window)
    sys.exit(exit_code)
