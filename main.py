"""Entry point for the news-image-20261120 bounty submission.

The front page for 20 November 2026 was drawn ahead of time by render.py
and stored as entry.png beside this file. The grader reads its output from
a directory ($MAKEFUN_OUTPUT_DIR, defaulting to /output), so this program
simply copies the stored image there under the expected name.

Standard library only, no network, deterministic: the bytes written are
exactly the bytes of the bundled entry.png.
"""

import os
import shutil
import sys
from pathlib import Path


def entry_image() -> Path:
    return Path(__file__).resolve().parent / "entry.png"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> int:
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(entry_image(), target_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
