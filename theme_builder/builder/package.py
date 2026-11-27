import json
import os
import shutil
import tempfile
import zipfile

from ..core.assets import DEFAULT_ICON
from ..core.settings import PACKAGE_NAME, ThemeSettings
from . import manifests, renderer


class ExtensionPackageBuilder:
    """Writes the video tab extension and companion theme into one ZIP."""

    ROOT_DIR = PACKAGE_NAME

    def __init__(self, settings: ThemeSettings):
        self.settings = settings

    def build(self, zip_path: str):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base_dir = os.path.join(tmp_dir, self.ROOT_DIR)
            self._write_video_tab(os.path.join(base_dir, "video-tab"))
            self._write_theme(os.path.join(base_dir, "my-theme"))
            self._zip_directory(base_dir, tmp_dir, zip_path)

    def _write_video_tab(self, target_dir: str):
        os.makedirs(target_dir)
        shutil.copy2(self.settings.video_path, os.path.join(target_dir, "video.mp4"))
        icon_filename = self._copy_icon(target_dir)

        self._write_json(target_dir, "manifest.json", manifests.video_tab_manifest(icon_filename))
        self._write_text(target_dir, "newtab.html", renderer.render_newtab_html(icon_filename))
        self._write_text(target_dir, "style.css", renderer.render_style_css(self.settings))
        self._write_text(target_dir, "script.js", renderer.render_script_js())

    def _write_theme(self, target_dir: str):
        os.makedirs(target_dir)
        self._write_json(target_dir, "manifest.json", manifests.theme_manifest(self.settings))

    def _copy_icon(self, target_dir: str) -> str:
        """Copy the chosen or default tab icon and return its new file name."""
        source = self.settings.icon_path or str(DEFAULT_ICON)
        ext = os.path.splitext(source)[1] or ".png"
        filename = f"icon{ext}"
        shutil.copy2(source, os.path.join(target_dir, filename))
        return filename

    @staticmethod
    def _write_text(folder: str, name: str, content: str):
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def _write_json(folder: str, name: str, data: dict):
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def _zip_directory(source_dir: str, relative_to: str, zip_path: str):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for folder_root, _, files in os.walk(source_dir):
                for file in files:
                    full_path = os.path.join(folder_root, file)
                    zf.write(full_path, os.path.relpath(full_path, relative_to))
