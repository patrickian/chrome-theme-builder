# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A PySide6 desktop app that turns an `.mp4` and a set of colors into a ZIP holding two unpacked Chrome items: `video-tab` (a Manifest V3 new tab override) and `my-theme` (a browser theme). See `README.md` for the user-facing description.

## Commands

Run from the repository root (Python 3.10+, developed on 3.11 and Windows):

```bash
pip install -r requirements.txt   # opencv-python is optional: live preview video only
python -m theme_builder

pip install -r requirements-build.txt
python scripts/build_exe.py       # portable Windows exe in dist/
```

There is no linter or test suite. Verify changes with throwaway scripts kept outside the repository.

## Architecture

Data flows one way: sidebar controls → `AppState.update(...)` → a new frozen `ThemeSettings` → `changed` signal → preview repaint. `MainWindow` (`app.py`) wires the signals, owns the dialogs and passes `AppState.settings` to `ExtensionPackageBuilder`.

- `core/` and `builder/` must not import any UI toolkit, so a ZIP can be built without a window.
- `builder/templates/` holds the generated page. The HTML and CSS use `string.Template`: `${name}` is filled by `renderer.py`, and a literal `$` must be `$$`. `script.js` is copied unchanged because its `${...}` is JavaScript.
- Bottom placements reuse the sidebar CSS and append `placement_bottom.css`, which reverses the column so the Add button stays at the bottom and the list grows upward.
- Only `media/video.py` uses OpenCV, behind an import guard.

## Things to keep in sync

- **Preview and generated page:** `ui/draw_shortcuts.py` repeats the pixel sizes from `builder/templates/*.css` on a 1280×720 design canvas, and `ui/draw_chrome.py` mirrors the color mapping in `builder/manifests.py`. Change both sides together.
- **Color labels:** the manifest sets `omnibox_background` from the *frame* color, although a sidebar label reads "Active tab & address bar". The README documents this.
- **Install steps:** `ui/howto.py` (in-app guide) and `README.md` describe the same steps. ZIP and folder names come from `PACKAGE_NAME` / `DEFAULT_ZIP_NAME` in `core/settings.py`.
- **Bundled files:** the exe only contains non-Python files listed in `DATA` in `scripts/build_exe.py`. Add any new asset or template location there. The version is `theme_builder.__version__`.
- **Default icon:** `core/assets.DEFAULT_ICON` is both the app icon and the tab icon used when the user picks none.

## Layout and styling

- The window's opening size is computed from `ControlsPanel.content_height()`, and the preview's bottom margin from `footer_line_offset()` so the preview ends level with the line above the contact footer. The preview is bottom-anchored and stays 16:9.
- Styles live in `ui/theme.py`. Sidebar widgets are styled through `#sidebar ...` selectors; a new sidebar rule needs that prefix to win over them.

## Scripting the app for verification

- Replace `theme_builder.ui.preferences._store` with a `QSettings` pointing at a temporary INI file; otherwise runs read and write the real registry.
- `main()` opens the guide as a modal dialog at startup. Start any exit timer only after `QApplication` exists (for example by wrapping `app.apply_theme`).
- If a script builds `MainWindow` itself, call `shiboken6.delete(window)` before exiting. Leaving it to interpreter shutdown can crash, which is why `main()` does the same. A launch stopped by timeout will not reveal this, so close the window and check the exit code.
- To check the generated new tab page, load the extracted `video-tab/newtab.html` in headless Chrome with a stub for `chrome.storage.local`.
