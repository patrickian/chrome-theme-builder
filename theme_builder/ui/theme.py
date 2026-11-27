"""Colors and style sheet for the builder's own window."""

from pathlib import Path

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

BACKGROUND = "#0f1117"
SURFACE = "#171a23"
SURFACE_HIGH = "#222632"
BORDER = "#2a2f3d"
TEXT = "#e8eaf2"
TEXT_MUTED = "#8c93a8"
ACCENT = "#5b8cff"
ACCENT_HOVER = "#7aa2ff"
CHEVRON = (Path(__file__).parent / "chevron.svg").as_posix()

STYLE_SHEET = f"""
QWidget {{ color: {TEXT}; font-family: "Segoe UI"; font-size: 13px; }}
QMainWindow, #root {{ background: {BACKGROUND}; }}
#sidebar, #sidebarBody {{ background: {SURFACE}; }}
#sidebar {{ border: none; border-right: 1px solid {BORDER}; }}

#appTitle {{ font-size: 15px; font-weight: 600; }}
#pageTitle {{ font-size: 15px; font-weight: 600; }}
#muted {{ color: {TEXT_MUTED}; font-size: 11px; }}
#section {{ color: {TEXT_MUTED}; font-size: 10px; font-weight: 700; letter-spacing: 1px; }}

#divider {{ background: {BORDER}; }}

#card {{ background: {BACKGROUND}; border: 1px solid {BORDER}; border-radius: 12px; }}

QPushButton {{
  background: {SURFACE_HIGH}; border: 1px solid {BORDER}; border-radius: 8px; padding: 6px 14px;
}}
QPushButton:hover {{ border-color: {ACCENT}; }}
QPushButton:pressed {{ background: {BORDER}; }}
QPushButton#primary {{
  background: {ACCENT}; border: none; color: white; font-size: 14px; font-weight: 600; padding: 12px;
}}
QPushButton#primary:hover {{ background: {ACCENT_HOVER}; }}

QPushButton#highlight {{
  background: {ACCENT}; border: none; border-radius: 6px; color: white;
  font-size: 12px; font-weight: 600; padding: 5px 12px;
}}
QPushButton#highlight:hover {{ background: {ACCENT_HOVER}; }}

QComboBox {{
  background: {SURFACE_HIGH}; border: 1px solid {BORDER}; border-radius: 8px; padding: 7px 10px;
}}
QComboBox:hover, QComboBox:focus {{ border-color: {ACCENT}; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox::down-arrow {{ image: url("{CHEVRON}"); width: 12px; height: 8px; }}
QComboBox QAbstractItemView {{
  background: {SURFACE_HIGH}; border: 1px solid {BORDER}; selection-background-color: {ACCENT}; outline: none;
}}

/* The sidebar uses smaller controls than the dialogs. */
#sidebar QLabel {{ font-size: 12px; }}
#sidebar QLabel#appTitle {{ font-size: 15px; }}
#sidebar QLabel#muted {{ font-size: 11px; }}
#sidebar QLabel#section {{ font-size: 10px; }}
#sidebar QPushButton {{ font-size: 12px; border-radius: 5px; padding: 3px 12px; }}
#sidebar QPushButton#swatch {{
  font-family: Consolas; font-size: 11px; padding: 3px 6px; text-align: left;
}}
#sidebar QPushButton#primary {{ font-size: 13px; border-radius: 6px; padding: 8px; }}
#sidebar QComboBox {{ font-size: 12px; border-radius: 5px; padding: 3px 8px; }}

QSlider::groove:horizontal {{ height: 4px; background: {BORDER}; border-radius: 2px; }}
QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 2px; }}
QSlider::handle:horizontal {{
  width: 12px; height: 12px; margin: -4px 0; border-radius: 6px; background: white;
}}

QScrollBar:vertical {{ width: 8px; background: transparent; }}
QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 4px; min-height: 30px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
"""


def apply_theme(app: QApplication):
    """Dark theme for the window and its dialogs."""
    app.setStyle("Fusion")

    palette = QPalette()
    for role, color in (
        (QPalette.Window, SURFACE),
        (QPalette.WindowText, TEXT),
        (QPalette.Base, BACKGROUND),
        (QPalette.AlternateBase, SURFACE),
        (QPalette.Text, TEXT),
        (QPalette.Button, SURFACE_HIGH),
        (QPalette.ButtonText, TEXT),
        (QPalette.Highlight, ACCENT),
        (QPalette.HighlightedText, "#ffffff"),
        (QPalette.ToolTipBase, SURFACE_HIGH),
        (QPalette.ToolTipText, TEXT),
        (QPalette.PlaceholderText, TEXT_MUTED),
    ):
        palette.setColor(role, QColor(color))
    app.setPalette(palette)
    app.setStyleSheet(STYLE_SHEET)
