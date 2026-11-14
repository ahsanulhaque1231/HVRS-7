"""Download the 300 HVRS-7 frames from the DriveAgent release on Hugging Face.

The frames are fetched from a pinned revision of the DriveAgent dataset
(https://huggingface.co/datasets/Parechan/driveagent), checked against
checksums/driveagent_r1_sha256.txt, and saved as F001.jpg ... F300.jpg.

Usage (from the repository root):
    python scripts/fetch_frames.py                 # saves to images/
    python scripts/fetch_frames.py --out tool/images   # ready for the annotation tool

Only the Python standard library is needed. Files that already exist with the
correct checksum are skipped, so the script can be re-run after an interruption.
"""
import argparse
import csv
import hashlib
import os
import sys
import time
import urllib.request

REPO = "Parechan/driveagent"
REVISION = "5dfff082e289cbe4729ce9960d90b7281c0eb4d3"  # DriveAgent revision used to build HVRS-7
URL = "https://huggingface.co/datasets/{repo}/resolve/{rev}/{path}"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="images", help="output folder (default: images)")
    ap.add_argument("--retries", type=int, default=3)
    args = ap.parse_args()

    index = list(csv.DictReader(open("annotations/frame_index.csv", newline="")))
    expected = {}
    for line in open("checksums/driveagent_r1_sha256.txt"):
        digest, path = line.split()
        expected[path] = digest

    os.makedirs(args.out, exist_ok=True)
    failed = []
    for n, row in enumerate(index, 1):
        dst = os.path.join(args.out, row["frame_id"] + ".jpg")
        want = expected[row["driveagent_file"]]
        if os.path.exists(dst) and sha256(open(dst, "rb").read()) == want:
            continue
        url = URL.format(repo=REPO, rev=REVISION, path=row["driveagent_file"])
        for attempt in range(1, args.retries + 1):
            try:
                data = urllib.request.urlopen(url, timeout=120).read()
                if sha256(data) != want:
                    raise ValueError("checksum mismatch")
                with open(dst, "wb") as f:
                    f.write(data)
                break
            except Exception as e:  # network error or checksum mismatch
                if attempt == args.retries:
                    failed.append((row["frame_id"], str(e)))
                else:
                    time.sleep(2 * attempt)
        print(f"\r{n}/{len(index)} frames", end="", flush=True)
    print()
    if failed:
        for fid, err in failed:
            print(f"FAILED {fid}: {err}", file=sys.stderr)
        sys.exit(1)
    print(f"All {len(index)} frames present in {args.out}/ and verified.")


if __name__ == "__main__":
    main()
