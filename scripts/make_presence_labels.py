"""Derive frame-level presence labels (300 x 7, 0/1) from the mark table.
A class is present in a frame if the frame has at least one mark of that class.
Usage: python scripts/make_presence_labels.py [annotations/marks.csv] [derived/presence_labels.csv]"""
import csv, sys
from collections import defaultdict
CLASSES = ["pedestrian", "four_wheel_vehicle", "non_four_wheel_vehicle", "sign",
           "fixed_installation", "plant", "monitor"]
src = sys.argv[1] if len(sys.argv) > 1 else "annotations/marks.csv"
dst = sys.argv[2] if len(sys.argv) > 2 else "derived/presence_labels.csv"
status = sys.argv[3] if len(sys.argv) > 3 else "annotations/frame_status.csv"
frames = [r["frame_id"] for r in csv.DictReader(open(status, newline=""))]
present = defaultdict(set)
for r in csv.DictReader(open(src, newline="")):
    present[r["frame_id"]].add(r["class_label"])
with open(dst, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["frame_id"] + CLASSES)
    for fid in sorted(frames):
        w.writerow([fid] + [int(c in present[fid]) for c in CLASSES])
print(f"wrote {dst}: {len(frames)} frames")
