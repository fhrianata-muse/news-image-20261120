#!/usr/bin/env python3
"""make.fun entry for news-image-20261120.

"Sum up 20 November's world news in one image": the program writes the
front page built in this repository (entry.png, drawn by make_image.py)
to the output directory as entry.png.

The front page covers Friday 20 November 2026: Russia's biggest
bombardment of the year on Kyiv (110 missiles, 400 drones, three Dnipro
bridges damaged) hours after the Trump-Xi-Putin peace declaration in
Shenzhen; the World Court ruling that Myanmar committed genocide
against the Rohingya; the global AI sell-off (S&P 500 -3.7%, Nikkei
-5.1%); Cyclone Akvan's landfall at Gopalpur, India; a tanker hit in
the Strait of Hormuz and Russian missiles in Poland; and the UK-EU
Brussels deals, with briefs on the Peru earthquake, BepiColombo at
Mercury, the Palisades Fire verdict and Haiti.

Standard library only, no network. Deterministic: every run writes
exactly the bytes of the shipped entry.png.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def locate_source():
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (os.path.join(here, SOURCE_NAME),
                      os.path.join(os.getcwd(), SOURCE_NAME),
                      os.path.join("/bot", SOURCE_NAME)):
        if os.path.isfile(candidate):
            return candidate
    return None


def main():
    src = locate_source()
    if src is None:
        print("error: entry.png not found next to main.py, in the "
              "working directory, or in /bot", file=sys.stderr)
        return 1

    # The gate accepts a whole PNG or JPEG of at most 1 MiB and
    # 1024x1024 pixels; refuse early if the shipped image ever breaks
    # those bounds instead of handing the grader an invalid entry.
    size = os.path.getsize(src)
    if size > 1048576:
        print(f"error: entry.png is {size} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        magic = fh.read(8)
    if magic[:8] != b"\x89PNG\r\n\x1a\n" and magic[:2] != b"\xff\xd8":
        print("error: entry.png is neither PNG nor JPEG data",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(src, dst)

    if os.path.getsize(src) != os.path.getsize(dst) or \
            digest(src) != digest(dst):
        os.remove(dst)
        print("error: written file differs from entry.png",
              file=sys.stderr)
        return 1

    print(f"ok: {dst} ({os.path.getsize(dst)} bytes, "
          f"sha256 {digest(dst)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
