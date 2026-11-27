from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter


def with_alpha(color: QColor, alpha: float) -> QColor:
    result = QColor(color)
    result.setAlphaF(alpha)
    return result


def fill_round_rect(p: QPainter, rect: QRectF, radius: float, fill: QColor, border: QColor | None = None):
    p.setPen(border if border is not None else Qt.NoPen)
    p.setBrush(fill)
    p.drawRoundedRect(rect, radius, radius)


def draw_text(
    p: QPainter,
    rect: QRectF,
    text: str,
    color: QColor,
    pixel_size: int,
    weight: QFont.Weight = QFont.Normal,
    align: Qt.AlignmentFlag = Qt.AlignLeft,
):
    """Draw one vertically centered line, elided if it does not fit."""
    font = QFont("Segoe UI")
    font.setPixelSize(pixel_size)
    font.setWeight(weight)
    font.setHintingPreference(QFont.PreferNoHinting)
    p.setFont(font)
    p.setPen(color)
    fitted = QFontMetricsF(font).elidedText(text, Qt.ElideRight, rect.width() + 1)
    p.drawText(rect, align | Qt.AlignVCenter, fitted)
