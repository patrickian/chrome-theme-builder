"""Paints the browser's tab strip and toolbar, in 1280px-wide design units."""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPen

from ..core.settings import ThemeSettings
from .paint_utils import draw_text, fill_round_rect, with_alpha

TAB_STRIP_H = 42
TOOLBAR_H = 46
CHROME_H = TAB_STRIP_H + TOOLBAR_H


def draw_chrome(p: QPainter, width: int, settings: ThemeSettings, icon: QImage | None):
    _draw_tab_strip(p, width, settings, icon)
    _draw_toolbar(p, width, settings)


def _draw_tab_strip(p: QPainter, width: int, settings: ThemeSettings, icon: QImage | None):
    text = QColor(settings.text_hex)
    p.fillRect(QRectF(0, 0, width, TAB_STRIP_H), QColor(settings.frame_hex))

    # Inactive tab
    fill_round_rect(p, QRectF(256, 8, 236, 30), 10, QColor(settings.inactive_tab_hex))
    p.setBrush(with_alpha(text, 0.35))
    p.setPen(Qt.NoPen)
    p.drawEllipse(QRectF(270, 15, 16, 16))
    draw_text(p, QRectF(296, 8, 150, 30), "Background Tab", with_alpha(text, 0.85), 12)
    _draw_cross(p, QPointF(472, 23), with_alpha(text, 0.7))

    # Active tab: rounded on top, flowing into the toolbar
    tab = QPainterPath()
    tab.moveTo(4, TAB_STRIP_H)
    tab.quadTo(14, TAB_STRIP_H, 14, TAB_STRIP_H - 10)
    tab.lineTo(14, 18)
    tab.quadTo(14, 8, 24, 8)
    tab.lineTo(240, 8)
    tab.quadTo(250, 8, 250, 18)
    tab.lineTo(250, TAB_STRIP_H - 10)
    tab.quadTo(250, TAB_STRIP_H, 260, TAB_STRIP_H)
    tab.closeSubpath()
    p.fillPath(tab, QColor(settings.toolbar_hex))

    icon_rect = QRectF(28, 17, 16, 16)
    if icon is not None:
        p.drawImage(icon_rect, icon)
    else:
        p.setBrush(with_alpha(text, 0.55))
        p.setPen(Qt.NoPen)
        p.drawEllipse(icon_rect)
    draw_text(p, QRectF(54, 10, 150, 30), "New Tab", text, 12)
    _draw_cross(p, QPointF(230, 25), text)

    # New tab "+" and window buttons
    p.setPen(_line_pen(text))
    p.drawLine(QPointF(506, 23), QPointF(518, 23))
    p.drawLine(QPointF(512, 17), QPointF(512, 29))

    p.drawLine(QPointF(width - 118, 20), QPointF(width - 108, 20))
    p.setBrush(Qt.NoBrush)
    p.drawRect(QRectF(width - 72, 15, 10, 10))
    _draw_cross(p, QPointF(width - 23, 20), text, 5)


def _draw_toolbar(p: QPainter, width: int, settings: ThemeSettings):
    text = QColor(settings.text_hex)
    y = TAB_STRIP_H
    mid = y + TOOLBAR_H / 2
    p.fillRect(QRectF(0, y, width, TOOLBAR_H), QColor(settings.toolbar_hex))

    _draw_arrow(p, 24, mid, -1, text)
    _draw_arrow(p, 60, mid, 1, with_alpha(text, 0.4))

    # Reload
    p.setPen(_line_pen(text))
    p.setBrush(Qt.NoBrush)
    p.drawArc(QRectF(89, mid - 7, 14, 14), 40 * 16, 290 * 16)
    p.drawLine(QPointF(102, mid - 7), QPointF(102, mid - 2))
    p.drawLine(QPointF(102, mid - 2), QPointF(97, mid - 2))

    # Address bar with a search glyph
    omnibox = QRectF(120, y + 6, width - 120 - 92, 34)
    fill_round_rect(p, omnibox, 17, QColor(settings.frame_hex))
    p.setPen(_line_pen(with_alpha(text, 0.7)))
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(QRectF(136, mid - 6, 10, 10))
    p.drawLine(QPointF(144.5, mid + 2.5), QPointF(149, mid + 7))
    draw_text(p, omnibox.adjusted(40, 0, -10, 0), "Search Google or type a URL", with_alpha(text, 0.75), 13)

    # Profile and menu
    p.setPen(Qt.NoPen)
    p.setBrush(with_alpha(text, 0.45))
    p.drawEllipse(QRectF(width - 74, mid - 11, 22, 22))
    p.setBrush(text)
    for offset in (-6, 0, 6):
        p.drawEllipse(QPointF(width - 24, mid + offset), 1.8, 1.8)


def _line_pen(color: QColor) -> QPen:
    return QPen(color, 1.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)


def _draw_cross(p: QPainter, center: QPointF, color: QColor, half: float = 4):
    p.setPen(_line_pen(color))
    p.drawLine(center + QPointF(-half, -half), center + QPointF(half, half))
    p.drawLine(center + QPointF(-half, half), center + QPointF(half, -half))


def _draw_arrow(p: QPainter, x: float, y: float, direction: int, color: QColor):
    """A back (-1) or forward (1) arrow centered on x, y."""
    p.setPen(_line_pen(color))
    tip = QPointF(x + 7 * direction, y)
    p.drawLine(QPointF(x - 7 * direction, y), tip)
    p.drawLine(tip, QPointF(x + direction, y - 6))
    p.drawLine(tip, QPointF(x + direction, y + 6))
