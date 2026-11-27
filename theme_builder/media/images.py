from PySide6.QtCore import QRectF, QSizeF, Qt
from PySide6.QtGui import QImage


def load_icon(path: str) -> QImage | None:
    """Return a small square icon image, or None if it cannot be loaded."""
    image = QImage(path)
    if image.isNull():
        return None
    # Scaling down smoothly here avoids jagged edges when it is painted.
    return image.scaled(32, 32, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)


def cover_source_rect(source: QSizeF, target: QSizeF) -> QRectF:
    """The centered part of `source` that fills `target` without stretching."""
    scale = max(target.width() / source.width(), target.height() / source.height())
    width, height = target.width() / scale, target.height() / scale
    return QRectF((source.width() - width) / 2, (source.height() - height) / 2, width, height)
