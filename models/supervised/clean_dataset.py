"""
Pre-training dataset cleaning for PerryVision.

Runs BEFORE dataset.py / train.py. Checks your data/platypus/ and data/perry/
folders for the kinds of problems that silently corrupt training rather than
crashing loudly:

  1. Corrupt / unreadable files      — anything that fails to open as an image
  2. Exact or near-duplicate images  — same photo saved twice, or trivial
                                        recompressions of the same photo
  3. Basic size/shape sanity stats   — flags if one class is made of much
                                        smaller or oddly-shaped images than
                                        the other, which can bias the model

This does NOT check whether an image is correctly labeled (i.e. whether a
Perry photo accidentally ended up in platypus/) — that still needs a human
eye. It also does not do "semantic" deduplication (two different photos of
the same specimen from slightly different angles are treated as different
images, which is correct — that's useful variety, not a duplicate).

Usage:
    python clean_dataset.py                # dry run — report only
    python clean_dataset.py --apply        # actually move flagged files

Flagged files are MOVED (never deleted) into a quarantine/ folder next to
data/, organized by class and reason, so nothing is destroyed by mistake.
"""

import argparse
import shutil
from collections import defaultdict
from pathlib import Path

from PIL import Image, UnidentifiedImageError

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
QUARANTINE_DIR = Path(__file__).resolve().parents[2] / "quarantine"
CLASS_NAMES = ["platypus", "perry"]

HASH_SIZE = 8  # 8x8 average hash — good enough to catch near-identical
               # images (resaves, minor recompression) without external deps


def average_hash(image: Image.Image) -> str:
    """A simple perceptual hash: shrink to 8x8 grayscale, compare each pixel
    to the mean brightness, encode as a bitstring. Near-identical images
    (even after resizing or mild recompression) tend to produce the same
    hash. This is NOT meant to catch two different photos of the same
    subject — only accidental duplicate files."""
    small = image.convert("L").resize((HASH_SIZE, HASH_SIZE), Image.LANCZOS)
    pixels = list(small.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join("1" if p >= avg else "0" for p in pixels)
    return bits


def check_class_folder(class_dir: Path):
    corrupt = []
    valid = []  # list of (path, PIL.Image, hash)
    sizes = []

    for path in sorted(class_dir.iterdir()):
        if not path.is_file():
            continue
        try:
            with Image.open(path) as img:
                img.verify()  # cheap structural check
            # Re-open after verify() — verify() leaves the file unusable for
            # further operations, so a fresh open is needed to actually hash it.
            with Image.open(path) as img:
                img = img.convert("RGB")
                h = average_hash(img)
                sizes.append(img.size)
                valid.append((path, h))
        except (UnidentifiedImageError, OSError):
            corrupt.append(path)

    return valid, corrupt, sizes


def find_duplicates(valid_entries):
    """Groups files by identical perceptual hash. Returns a list of groups
    (each a list of paths) where more than one file shares a hash."""
    by_hash = defaultdict(list)
    for path, h in valid_entries:
        by_hash[h].append(path)
    return [paths for paths in by_hash.values() if len(paths) > 1]


def print_size_stats(class_name: str, sizes: list):
    if not sizes:
        print(f"  {class_name}: no valid images to measure")
        return
    widths = [w for w, _ in sizes]
    heights = [h for _, h in sizes]
    aspect_ratios = [w / h for w, h in sizes]
    print(
        f"  {class_name}: {len(sizes)} images | "
        f"width {min(widths)}-{max(widths)}px | "
        f"height {min(heights)}-{max(heights)}px | "
        f"aspect ratio {min(aspect_ratios):.2f}-{max(aspect_ratios):.2f}"
    )


def quarantine_file(path: Path, class_name: str, reason: str, apply: bool):
    dest_dir = QUARANTINE_DIR / class_name / reason
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    if apply:
        shutil.move(str(path), str(dest))
    return dest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move flagged files to quarantine/. Without this flag, "
        "the script only reports what it would do.",
    )
    args = parser.parse_args()

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"No data/ directory found at {DATA_DIR}")

    print(f"{'Applying changes' if args.apply else 'DRY RUN (no files will be moved)'}\n")

    total_corrupt = 0
    total_dupe_files = 0

    for class_name in CLASS_NAMES:
        class_dir = DATA_DIR / class_name
        if not class_dir.exists():
            print(f"⚠ Skipping '{class_name}' — folder not found at {class_dir}")
            continue

        print(f"--- {class_name} ---")
        valid, corrupt, sizes = check_class_folder(class_dir)

        # Corrupt files
        if corrupt:
            print(f"  ✗ {len(corrupt)} corrupt/unreadable file(s):")
            for path in corrupt:
                dest = quarantine_file(path, class_name, "corrupt", args.apply)
                print(f"      {path.name} → {dest if args.apply else '(would move to) ' + str(dest)}")
            total_corrupt += len(corrupt)
        else:
            print("  ✓ No corrupt files found")

        # Duplicates
        dupe_groups = find_duplicates(valid)
        if dupe_groups:
            print(f"  ✗ {len(dupe_groups)} group(s) of duplicate/near-duplicate images:")
            for group in dupe_groups:
                keeper, extras = group[0], group[1:]
                print(f"      keeping {keeper.name}, flagging {len(extras)} duplicate(s):")
                for path in extras:
                    dest = quarantine_file(path, class_name, "duplicate", args.apply)
                    print(f"        {path.name} → {dest if args.apply else '(would move to) ' + str(dest)}")
                    total_dupe_files += 1
        else:
            print("  ✓ No duplicates found")

        print_size_stats(class_name, sizes)
        print()

    print("=== Summary ===")
    print(f"Corrupt files flagged: {total_corrupt}")
    print(f"Duplicate files flagged: {total_dupe_files}")
    if not args.apply and (total_corrupt or total_dupe_files):
        print("\nThis was a dry run — rerun with --apply to actually move these files.")


if __name__ == "__main__":
    main()