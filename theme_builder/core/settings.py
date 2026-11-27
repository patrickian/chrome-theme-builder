from dataclasses import dataclass

PACKAGE_NAME = "theme-extensions"  # the folder inside the ZIP
DEFAULT_ZIP_NAME = f"{PACKAGE_NAME}.zip"

CENTER_PLACEMENT = "Center (Grid)"

PLACEMENTS = [
    "Top-Right (Vertical)",
    "Top-Left (Vertical)",
    "Bottom-Right (Vertical)",
    "Bottom-Left (Vertical)",
    CENTER_PLACEMENT,
]


@dataclass(frozen=True)
class ThemeSettings:
    """Everything the user can choose, with the app's default values."""

    video_path: str = ""
    icon_path: str = ""
    frame_hex: str = "#12141c"
    inactive_tab_hex: str = "#161923"
    toolbar_hex: str = "#1c202b"
    text_hex: str = "#ffffff"
    btn_bg_hex: str = "#14141a"
    btn_opacity: float = 0.35
    placement: str = PLACEMENTS[0]
