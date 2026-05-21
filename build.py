import os
import sys
from pathlib import Path

import PyInstaller.__main__


PROJECT_ROOT = Path(__file__).resolve().parent


def add_data_arg(source: Path, destination: str) -> str:
    sep = ";" if sys.platform == "win32" else ":"
    return f"{source}{sep}{destination}"


def build():
    style_file = PROJECT_ROOT / "MusicTager" / "ui" / "style.qss"
    config_file = PROJECT_ROOT / "config.json"
    image_folder = PROJECT_ROOT / "image-folder"
    entry_file = PROJECT_ROOT / "MusicTager" / "main.py"

    for path in (entry_file, style_file, config_file, image_folder):
        if not path.exists():
            raise FileNotFoundError(f"Build resource not found: {path}")

    PyInstaller.__main__.run([
        str(entry_file),
        "--onefile",
        "--windowed",
        "--name",
        "MusicTagger",
        "--clean",
        "--add-data",
        add_data_arg(style_file, "ui"),
        "--add-data",
        add_data_arg(style_file, os.path.join("MusicTager", "ui")),
        "--add-data",
        add_data_arg(config_file, "."),
        "--add-data",
        add_data_arg(image_folder, "image-folder"),
        # "--icon", str(PROJECT_ROOT / "MusicTager" / "icon.ico"),
    ])

    print("\nBuild complete.")
    print("Executable: dist/MusicTagger.exe")


if __name__ == "__main__":
    build()
