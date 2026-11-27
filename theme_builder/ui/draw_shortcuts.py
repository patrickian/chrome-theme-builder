"""Paints sample shortcuts using the sizes in the generated style sheet."""

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen

from ..core.settings import CENTER_PLACEMENT, ThemeSettings
from .paint_utils import draw_text, fill_round_rect

SAMPLE_SHORTCUTS = [("YouTube", "#ff3b30"), ("GitHub", "#6e7681"), ("Gmail", "#ea8f00")]


def draw_shortcuts(p: QPainter, page: QRectF, settings: ThemeSettings):
    """`page` is the visible web page area, in CSS pixels."""
    if settings.placement == CENTER_PLACEMENT:
        _draw_grid(p, page, settings)
    else:
        _draw_sidebar(p, page, settings)


def _button(p: QPainter, rect: QRectF, settings: ThemeSettings, border_alpha: int):
    fill = QColor(settings.btn_bg_hex)
    fill.setAlphaF(settings.btn_opacity)
    fill_round_rect(p, rect, 10, fill, QPen(QColor(255, 255, 255, border_alpha), 1))


def _icon(p: QPainter, rect: QRectF, radius: float, size: float, name: str, color: str):
    """The tinted icon holder with a lettered stand-in for the site's favicon."""
    fill_round_rect(p, rect, radius, QColor(255, 255, 255, 31))
    inner = QRectF(0, 0, size, size)
    inner.moveCenter(rect.center())
    fill_round_rect(p, inner, 3, QColor(color))
    draw_text(p, inner, name[0], QColor("white"), int(size * 0.7), QFont.Bold, Qt.AlignHCenter)


def _add_button(p: QPainter, rect: QRectF, settings: ThemeSettings):
    _button(p, rect, settings, 56)
    draw_text(
        p, rect, "+ Add Shortcut", QColor(settings.text_hex), 13, QFont.DemiBold, Qt.AlignHCenter
    )


def _draw_sidebar(p: QPainter, page: QRectF, settings: ThemeSettings):
    inset, width = 16, 210
    add_h, row_h, add_gap, row_gap = 37, 44, 8, 7
    x = page.left() + inset if "Left" in settings.placement else page.right() - inset - width

    # Bottom placements keep the Add button at the bottom and stack rows upward.
    upward = "Bottom" in settings.placement
    add_y = page.bottom() - inset - add_h if upward else page.top() + inset
    _add_button(p, QRectF(x, add_y, width, add_h), settings)

    y = add_y - add_gap - row_h if upward else add_y + add_h + add_gap
    step = -(row_h + row_gap) if upward else row_h + row_gap
    for name, color in SAMPLE_SHORTCUTS:
        row = QRectF(x, y, width, row_h)
        _button(p, row, settings, 46)
        _icon(p, QRectF(x + 11, y + 9, 26, 26), 7, 16, name, color)
        draw_text(p, row.adjusted(47, 0, -56, 0), name, QColor(settings.text_hex), 13, QFont.Medium)
        y += step


def _draw_grid(p: QPainter, page: QRectF, settings: ThemeSettings):
    add_w, add_h, card, gap, row_gap = 150, 37, 108, 14, 16
    count = len(SAMPLE_SHORTCUTS)
    list_w = count * card + (count - 1) * gap
    list_h = card + 8  # the list's 4px padding
    y = page.center().y() - (add_h + row_gap + list_h) / 2

    _add_button(p, QRectF(page.center().x() - add_w / 2, y, add_w, add_h), settings)
    y += add_h + row_gap + 4
    x = page.center().x() - list_w / 2
    for name, color in SAMPLE_SHORTCUTS:
        _button(p, QRectF(x, y, card, card), settings, 46)
        _icon(p, QRectF(x + (card - 40) / 2, y + 22, 40, 40), 20, 22, name, color)
        draw_text(
            p, QRectF(x + 8, y + 70, card - 16, 20), name, QColor(settings.text_hex), 13,
            QFont.Medium, Qt.AlignHCenter,
        )
        x += card + gap
