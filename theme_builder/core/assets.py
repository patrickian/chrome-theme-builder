from pathlib import Path

_ASSETS = Path(__file__).resolve().parent.parent / "assets"

# The app's logo, also used as the tab icon when the user picks none.
DEFAULT_ICON = _ASSETS / "icon.png"

# Shown with the contact address at the bottom of the sidebar.
BRAND_LOGO = _ASSETS / "brand.png"

# Shown beside the title at the top of the sidebar.
CHROME_LOGO = _ASSETS / "chrome.svg"
