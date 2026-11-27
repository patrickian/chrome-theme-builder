"""Fills the web templates in `templates/` with the user's settings."""

from pathlib import Path
from string import Template

from ..core.colors import hex_to_rgb
from ..core.settings import CENTER_PLACEMENT, ThemeSettings

TEMPLATE_DIR = Path(__file__).parent / "templates"

# Bottom placements differ only in their stacking order (placement_bottom.css).
_SIDEBAR_POSITIONS = {
    "Top-Right (Vertical)": "top: 16px; right: 16px; bottom: 16px;",
    "Top-Left (Vertical)": "top: 16px; left: 16px; bottom: 16px;",
    "Bottom-Right (Vertical)": "top: 16px; right: 16px; bottom: 16px;",
    "Bottom-Left (Vertical)": "top: 16px; left: 16px; bottom: 16px;",
}


def _read(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def _fill(name: str, **values) -> str:
    return Template(_read(name)).substitute(values)


def render_newtab_html(icon_filename: str = "") -> str:
    icon_link = f'<link rel="icon" href="{icon_filename}">' if icon_filename else ""
    return _fill("newtab.html", icon_link=icon_link)


def render_placement_css(placement: str) -> str:
    if placement == CENTER_PLACEMENT:
        return _read("placement_center.css")
    css = _fill("placement_sidebar.css", position=_SIDEBAR_POSITIONS[placement])
    if placement.startswith("Bottom"):
        css += _read("placement_bottom.css")
    return css


def render_style_css(settings: ThemeSettings) -> str:
    btn_r, btn_g, btn_b = hex_to_rgb(settings.btn_bg_hex)
    alpha = round(settings.btn_opacity, 2)
    return _fill(
        "style.css",
        btn_r=btn_r,
        btn_g=btn_g,
        btn_b=btn_b,
        alpha=alpha,
        hover_alpha=min(0.95, round(alpha + 0.25, 2)),
        txt_hex=settings.text_hex,
        placement_css=render_placement_css(settings.placement),
    )


def render_script_js() -> str:
    # Not templated: the `${...}` in this file belongs to JavaScript.
    return _read("script.js")
