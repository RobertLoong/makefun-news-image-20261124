#!/usr/bin/env python3
"""Entry for make.fun's "Sum up 24 November's world news in one image".

The poster (poster.png, 1024x1024, built by make_poster.py from the day's
wire reports) ships in this repository. This program copies it, byte for
byte, to /output/entry.png. Pure standard library, no network, no clock,
no randomness: two runs write identical bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "poster.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def png_dimensions(path):
    """Read width/height from a PNG IHDR chunk with the standard library."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        print("poster.png missing next to main.py", file=sys.stderr)
        return 1
    width, height = png_dimensions(SOURCE)
    if width > 1024 or height > 1024:
        print(f"poster too large: {width}x{height}", file=sys.stderr)
        return 1
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    size = os.path.getsize(DEST)
    digest = hashlib.sha256(open(DEST, "rb").read()).hexdigest()
    if size > 1024 * 1024:
        print(f"entry.png too large: {size} bytes", file=sys.stderr)
        return 1
    print(f"wrote {DEST} ({width}x{height}, {size} bytes, "
          f"sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
