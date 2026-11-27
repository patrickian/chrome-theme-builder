from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QImage

try:
    import cv2
except ImportError:
    cv2 = None


class VideoPlayer(QObject):
    """Loops a video, keeping the latest frame as a QImage."""

    frame_changed = Signal()

    def __init__(self):
        super().__init__()
        self._cap = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._next_frame)
        self.frame: QImage | None = None

    @staticmethod
    def is_available() -> bool:
        return cv2 is not None

    def stop(self):
        self._timer.stop()
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def start(self, path: str):
        self.stop()
        self.frame = None
        self.frame_changed.emit()
        if not self.is_available():
            return

        self._cap = cv2.VideoCapture(path)
        fps = self._cap.get(cv2.CAP_PROP_FPS)
        self._timer.start(int(1000 / fps) if fps and 5 <= fps <= 60 else 33)
        self._next_frame()

    def _next_frame(self):
        if self._cap is None:
            return
        ok, frame = self._cap.read()
        if not ok or frame is None:
            # Loop back to start of video
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self._cap.read()

        if ok and frame is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width = rgb.shape[:2]
            # copy() so the image does not point into the array after it is freed
            self.frame = QImage(rgb.data, width, height, rgb.strides[0], QImage.Format_RGB888).copy()
            self.frame_changed.emit()
