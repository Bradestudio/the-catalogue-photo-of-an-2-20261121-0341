#!/usr/bin/env python3
"""Copy the STRAIGHT-O-MATIC catalogue photo to the output directory.

The entry image is a studio catalogue photograph of an impossible
gadget: the STRAIGHT-O-MATIC banana straightener, a brushed-steel
countertop machine with chrome rollers. A ripe curved banana is
caught halfway through the rollers, and the same banana comes out
of the far side perfectly straight. One straight banana lies beside
the machine as the finished result, the proof of what the gadget
does. The joke reads at a glance, with no caption at all: curved
in, straight out.

This program does nothing to the picture itself. It reads the PNG
shipped next to this script, checks that it really is a PNG and
that it fits inside the size and dimension gates for the bounty,
copies it byte for byte to the output directory, and then reads the
copy back to prove the two files are identical. Standard library
only, no network, no clock, no randomness.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"

USAGE = (
    "usage: python3 main.py [output-dir]\n"
    "Copy entry.png byte for byte to [output-dir]/entry.png.\n"
    "Without an argument, MAKEFUN_OUTPUT_DIR is used, then /output\n"
    "when it exists, otherwise an 'output' folder."
)


def read_png_dimensions(data):
    """Return the (width, height) stored in a PNG's IHDR chunk.

    The first bytes must be the PNG signature and the first chunk
    must be IHDR; anything else is rejected instead of guessed at.
    """
    if len(data) < 33 or not data.startswith(PNG_SIGNATURE):
        raise ValueError("source file is not a PNG image")
    chunk_length = struct.unpack(">I", data[8:12])[0]
    chunk_type = data[12:16]
    if chunk_type != b"IHDR" or chunk_length != 13:
        raise ValueError("PNG file has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def resolve_output_dir(argv):
    """Pick where the copy goes.

    An explicit argument wins, then the MAKEFUN_OUTPUT_DIR
    environment variable, then /output when it exists, and finally
    a plain "output" folder next to the current directory.
    """
    if len(argv) > 1:
        return argv[1]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return "output"


def main(argv):
    if len(argv) > 1 and argv[1] in ("-h", "--help"):
        print(USAGE)
        return 0

    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    with open(source, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        raise SystemExit(
            "entry.png is %d bytes, over the %d byte limit"
            % (len(data), MAX_BYTES)
        )

    width, height = read_png_dimensions(data)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise SystemExit(
            "entry.png is %dx%d, over the %dx%d limit"
            % (width, height, MAX_WIDTH, MAX_HEIGHT)
        )

    output_dir = resolve_output_dir(argv)
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, SOURCE_NAME)

    with open(destination, "wb") as handle:
        handle.write(data)

    with open(destination, "rb") as handle:
        copied = handle.read()
    if copied != data:
        raise SystemExit("copy does not match the source byte for byte")

    digest = hashlib.sha256(data).hexdigest()
    print(
        "%s %d bytes %dx%d sha256=%s"
        % (destination, len(data), width, height, digest)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
