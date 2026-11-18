#!/usr/bin/env python3
"""News-image entry for make.fun competition news-image-20261117.

Reads the front-page image beside this file (entry.png), checks that it is
a whole PNG of at most 1 MiB and at most 1024 by 1024 pixels, then copies
its exact bytes to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when
the variable is unset). Standard library only; no network. The copy is
byte-identical on every run.

Run outside the grader's container with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_DIM = 1024
MIN_BYTES = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"main.py: {message}", file=sys.stderr)
    return 1


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        return fail(f"missing image: {source}")
    data = source.read_bytes()
    if len(data) < MIN_BYTES:
        return fail(f"image too small ({len(data)} bytes), likely truncated")
    if len(data) > MAX_BYTES:
        return fail(f"image too big ({len(data)} bytes > {MAX_BYTES})")
    if data[:8] != PNG_SIGNATURE:
        return fail("image is not a PNG (bad signature)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("image has no PNG IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        return fail(f"image too large ({width}x{height} > {MAX_DIM}x{MAX_DIM})")
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return fail("image lacks a whole PNG IEND trailer")
    if b"IDAT" not in data:
        return fail("image has no PNG image data (IDAT chunk)")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} {len(data)} bytes {width}x{height} "
          f"sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
