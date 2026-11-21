#!/usr/bin/env python3
"""Entrypoint for the make.fun the-catalogue-photo-of-an-2-20261121-0341 entry.

Writes one catalogue photograph to /output/entry.png: the STRAIGHT-O-MATIC
banana straightener, a small countertop gadget caught mid-use -- a curved
banana goes in through the chrome rollers on the left and comes out
perfectly straight on the right. One perfectly straight banana lies
beside the machine as the single accessory: the finished result. Stdlib
only, no network, no clock, no randomness: the program copies the entry
image shipped in this repository byte for byte, so every run writes the
exact same bytes.

The photograph (1024x1024 PNG, 462,246 bytes):
- Hero: brushed-steel and matte-cream countertop machine with chrome
  rollers and a printed "STRAIGHT-O-MATIC" brand label, on a seamless
  pale-grey studio background with soft diffused light and a gentle
  shadow -- a real catalogue product shot.
- Mid-use: a ripe curved banana is halfway through the rollers; the
  same banana emerges from the far side perfectly straight.
- One accessory: a single straight banana lying beside the machine,
  the proof of what the gadget does.
- The joke reads at a glance, with no caption: curved in, straight out.
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def png_dimensions(data):
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        raise SystemExit("entry.png has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    dest = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not dest and len(sys.argv) > 1:
        dest = sys.argv[1]
    if not dest:
        dest = "/output" if Path("/output").is_dir() else "output"
    outdir = Path(dest)
    outdir.mkdir(parents=True, exist_ok=True)
    target = outdir / "entry.png"
    shutil.copyfile(ASSET, target)
    data = target.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, gate needs "
                         f"at most {MAX_BYTES}")
    width, height = png_dimensions(data)
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"entry.png is {width}x{height}, gate needs "
                         f"at most {MAX_DIM}x{MAX_DIM}")
    if data != ASSET.read_bytes():
        raise SystemExit("copied entry.png differs from the shipped asset")
    print(f"wrote {target} ({len(data)} bytes, {width}x{height}, "
          f"sha256 {hashlib.sha256(data).hexdigest()})")


if __name__ == "__main__":
    main()
