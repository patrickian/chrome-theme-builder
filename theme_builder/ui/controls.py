from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ..core.assets import CHROME_LOGO
from ..core.settings import DEFAULT_ZIP_NAME, PLACEMENTS
from .footer import BrandFooter
from .state import AppState
from .widgets import ColorRow, FileRow, make_divider, make_label

# Sidebar spacing, in pixels
EDGE = 16  # left and right margin
SECTION_GAP = 12  # above and below the line between sections
ROW_GAP = 6  # between rows inside a section
LABEL_W = 56  # lines up the shortcut controls
BOTTOM = 10  # below the contact area
TITLE_ICON = 20  # size of the logo beside the title
FOOTER_GAP = 10  # between the items under the settings

COLOR_FIELDS = [
    ("frame_hex", "Browser frame / sidebar"),
    ("inactive_tab_hex", "Inactive tabs"),
    ("toolbar_hex", "Active tab & address bar"),
    ("text_hex", "Browser & shortcut text"),
    ("btn_bg_hex", "Shortcut button tint"),
]


class ControlsPanel(QFrame):
    """Left sidebar: settings, the build button, and the logo with contact details."""

    pick_video_requested = Signal()
    pick_icon_requested = Signal()
    generate_requested = Signal()

    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.setObjectName("sidebar")
        self.setFixedWidth(320)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        body = QWidget()
        body.setObjectName("sidebarBody")
        scroll.setWidget(body)

        layout = QVBoxLayout(body)
        layout.setContentsMargins(EDGE, 14, EDGE, BOTTOM)
        layout.setSpacing(0)

        layout.addLayout(self._build_title())
        layout.addSpacing(2)
        layout.addWidget(make_label("Video new tab page and matching Chrome theme", "muted"))

        self._add_section(layout, "MEDIA", self._media_rows())
        self._add_section(layout, "COLORS", self._color_rows())
        self._add_section(layout, "SHORTCUTS", self._shortcut_rows())
        layout.addSpacing(SECTION_GAP)
        layout.addLayout(self._build_footer(), 1)
        self._body = body

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        state.changed.connect(self._show_file_names)

    def _build_title(self) -> QHBoxLayout:
        logo = make_label("")
        logo.setPixmap(
            QIcon(str(CHROME_LOGO)).pixmap(QSize(TITLE_ICON, TITLE_ICON), self.devicePixelRatioF())
        )
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(logo)
        row.addWidget(make_label("Theme Builder", "appTitle"), 1)
        return row

    def _build_footer(self) -> QVBoxLayout:
        """The build button under the settings, and the contact details at the bottom."""
        build_btn = QPushButton(f"Generate {DEFAULT_ZIP_NAME}")
        build_btn.setObjectName("primary")
        build_btn.setCursor(Qt.PointingHandCursor)
        build_btn.clicked.connect(self.generate_requested)

        footer = QVBoxLayout()
        footer.setSpacing(FOOTER_GAP)
        footer.addWidget(make_divider())
        footer.addWidget(build_btn)
        footer.addSpacing(25)  # the least space kept above the contact area
        footer.addStretch(1)  # spare height goes here, keeping the contact area at the bottom
        footer.addWidget(make_divider())
        self._brand = BrandFooter()
        footer.addWidget(self._brand)
        return footer

    def content_height(self) -> int:
        """The height needed to show everything without scrolling."""
        return self._body.sizeHint().height()

    def footer_line_offset(self) -> int:
        """Distance from the sidebar's bottom up to the line above the contact area."""
        return BOTTOM + self._brand.sizeHint().height() + FOOTER_GAP

    @staticmethod
    def _add_section(layout: QVBoxLayout, title: str, rows: list[QWidget]):
        layout.addSpacing(SECTION_GAP)
        layout.addWidget(make_divider())
        layout.addSpacing(SECTION_GAP)
        layout.addWidget(make_label(title, "section"))
        for row in rows:
            layout.addSpacing(ROW_GAP)
            layout.addWidget(row)

    def _media_rows(self) -> list[QWidget]:
        self._video_row = FileRow("Background video", "No .mp4 selected")
        self._video_row.browse_requested.connect(self.pick_video_requested)
        self._icon_row = FileRow("Tab icon (optional)", "Default: NT logo")
        self._icon_row.browse_requested.connect(self.pick_icon_requested)
        return [self._video_row, self._icon_row]

    def _color_rows(self) -> list[QWidget]:
        rows = []
        for field, title in COLOR_FIELDS:
            row = ColorRow(title, getattr(self.state.settings, field))
            row.color_picked.connect(lambda color, field=field: self.state.update(**{field: color}))
            rows.append(row)
        return rows

    def _shortcut_rows(self) -> list[QWidget]:
        placement = QComboBox()
        placement.addItems(PLACEMENTS)
        placement.setCurrentText(self.state.settings.placement)
        placement.currentTextChanged.connect(lambda text: self.state.update(placement=text))

        # The slider works in whole percent; the settings store 0.1 - 0.9.
        slider = QSlider(Qt.Horizontal)
        slider.setRange(10, 90)
        slider.setValue(round(self.state.settings.btn_opacity * 100))
        value_label = make_label(f"{slider.value()}%", "muted")
        value_label.setFixedWidth(30)
        value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        def on_opacity(percent: int):
            value_label.setText(f"{percent}%")
            self.state.update(btn_opacity=percent / 100)

        slider.valueChanged.connect(on_opacity)

        return [
            self._labelled_row("Position", placement),
            self._labelled_row("Opacity", slider, value_label),
        ]

    @staticmethod
    def _labelled_row(title: str, control: QWidget, trailing: QWidget | None = None) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        label = make_label(title)
        label.setFixedWidth(LABEL_W)
        layout.addWidget(label)
        layout.addWidget(control, 1)
        if trailing is not None:
            layout.addWidget(trailing)
        return row

    def _show_file_names(self):
        self._video_row.set_path(self.state.settings.video_path)
        self._icon_row.set_path(self.state.settings.icon_path)
