from ..core.colors import hex_to_rgb
from ..core.settings import ThemeSettings


def video_tab_manifest(icon_filename: str = "") -> dict:
    manifest = {
        "manifest_version": 3,
        "name": "My Video Tab",
        "version": "1.0",
        "permissions": ["storage"],
        "chrome_url_overrides": {"newtab": "newtab.html"},
    }
    if icon_filename:
        manifest["icons"] = {size: icon_filename for size in ("16", "48", "128")}
    return manifest


def theme_manifest(settings: ThemeSettings) -> dict:
    frame_rgb = hex_to_rgb(settings.frame_hex)
    inactive_rgb = hex_to_rgb(settings.inactive_tab_hex)
    toolbar_rgb = hex_to_rgb(settings.toolbar_hex)
    text_rgb = hex_to_rgb(settings.text_hex)

    return {
        "manifest_version": 3,
        "name": "My Video Companion Theme",
        "version": "1.0",
        "theme": {
            "colors": {
                "frame": frame_rgb,
                "frame_inactive": frame_rgb,
                "frame_incognito": frame_rgb,
                "frame_incognito_inactive": frame_rgb,
                "background_tab": inactive_rgb,
                "background_tab_inactive": inactive_rgb,
                "toolbar": toolbar_rgb,
                "tab_text": text_rgb,
                "tab_background_text": text_rgb,
                "tab_background_text_inactive": text_rgb,
                "bookmark_text": text_rgb,
                "omnibox_background": frame_rgb,
                "omnibox_text": text_rgb,
                "toolbar_button_icon": text_rgb,
                "ntp_background": frame_rgb,
            }
        },
    }
