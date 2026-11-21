# Build report — the-catalogue-photo-of-an-2-20261121-0341 (round 1)

- Bounty: "The Catalogue Photo of an Impossible Gadget", $20 total
  (20 winners × $1), free, opened 2026-11-21 03:41 UTC, deadline
  2026-11-21 04:41 UTC (11:41 WIB).
- Gadget: the STRAIGHT-O-MATIC banana straightener. A curved banana
  goes in through the chrome rollers and comes out perfectly straight;
  the single accessory is one straight banana lying beside the machine.
  The joke reads at a glance: curved in, straight out.
- Image: photorealistic studio catalogue shot, generated, then resized
  to 1024×1024. v1 had the accessory banana cropped at the right edge;
  v2 re-framed it (still very slightly at the edge) and was kept.
- Entry: `entry.png`, 1024×1024 PNG, 462,246 bytes,
  sha256 a341c9ba9a93cfe08a3a831ea846344864d87e6ba570eb1a8b9fa1a805d23356.
- `main.py` (Python 3.13, stdlib only, no network) copies the shipped
  image byte for byte to `/output/entry.png`. Two runs verified
  byte-identical (same sha256, `cmp` clean).
- Kit: `makefun check` run from the unpacked dev kit; see the check
  log. Transcripts bundled with `makefun bundle` (see bundle log);
  the record command ran in the background during the build.
- NOT submitted by this builder; parent submits.
