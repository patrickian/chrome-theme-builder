"""Builds the portable Windows exe: python scripts/build_exe.py"""

import os
import sys
from pathlib import Path

import PyInstaller.__main__

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from theme_builder import __version__  # noqa: E402
from theme_builder.core.assets import DEFAULT_ICON  # noqa: E402

APP_NAME = "ChromeThemeBuilder"
PRODUCT_NAME = "Chrome Video Tab & Theme Builder"

# Files the app reads at run time, bundled at the same relative paths.
DATA = [
    ("theme_builder/assets", "theme_builder/assets"),
    ("theme_builder/builder/templates", "theme_builder/builder/templates"),
    ("theme_builder/ui/chevron.svg", "theme_builder/ui"),
]

# The details Windows shows under the exe's Properties > Details.
VERSION_INFO = """VSVersionInfo(
  ffi=FixedFileInfo(filevers={numbers}, prodvers={numbers}),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('FileDescription', {product!r}),
      StringStruct('FileVersion', {version!r}),
      StringStruct('InternalName', {name!r}),
      StringStruct('OriginalFilename', {filename!r}),
      StringStruct('ProductName', {product!r}),
      StringStruct('ProductVersion', {version!r}),
    ])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])]),
  ],
)
"""


def build(entry: Path = ROOT / "scripts" / "launcher.py", name: str = APP_NAME,
          dist: Path = ROOT / "dist", work: Path = ROOT / "build"):
    """Packs `entry` and everything it needs into the single file dist/<name>.exe."""
    work.mkdir(parents=True, exist_ok=True)
    version_file = work / "version_info.txt"
    numbers = tuple(int(part) for part in __version__.split(".")) + (0,)
    version_file.write_text(
        VERSION_INFO.format(
            numbers=numbers,
            version=__version__,
            name=name,
            filename=f"{name}.exe",
            product=PRODUCT_NAME,
        ),
        encoding="utf-8",
    )

    args = [
        str(entry),
        "--name", name,
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--icon", str(DEFAULT_ICON),
        "--version-file", str(version_file),
        "--paths", str(ROOT),
        "--distpath", str(dist),
        "--workpath", str(work),
        "--specpath", str(work),
    ]
    for source, target in DATA:
        args += ["--add-data", f"{ROOT / source}{os.pathsep}{target}"]
    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    if sys.platform != "win32":
        sys.exit("Build the exe on Windows: PyInstaller cannot cross-compile.")
    build()
