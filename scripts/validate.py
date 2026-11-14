"""Consistency checks for HVRS-7. Exit code 0 if all checks pass.
Usage: python scripts/validate.py   (run from the repository root)"""
import csv
import json
import sys

CLASSES = ["pedestrian", "four_wheel_vehicle", "non_four_wheel_vehicle", "sign",
           "fixed_installation", "plant", "monitor"]
rd = lambda p: list(csv.DictReader(open(p, newline="")))
marks = rd("annotations/marks.csv")
status = {r["frame_id"]: r for r in rd("annotations/frame_status.csv")}
index = {r["frame_id"]: r for r in rd("annotations/frame_index.csv")}
presence = {r["frame_id"]: r for r in rd("derived/presence_labels.csv")}
backup = json.load(open("annotations/tool_backup.json"))["frames"]
sums = dict(reversed(l.split()) for l in open("checksums/driveagent_r1_sha256.txt"))

checks = []
def check(name, ok):
    checks.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + name)

check("300 frames in status, index, presence labels and tool backup",
      len(status) == len(index) == len(presence) == len(backup) == 300)
check("every mark has a known class", all(m["class_label"] in CLASSES for m in marks))
check("every mark is a point or a box", all(m["annotation_type"] in ("point", "box") for m in marks))
check("boxes have a size, points do not",
      all((m["width_norm"] != "") == (m["annotation_type"] == "box") for m in marks))
check("normalized coordinates within [0, 1]",
      all(0 <= float(m["x_norm"]) <= 1 and 0 <= float(m["y_norm"]) <= 1 for m in marks))
check("(frame_id, annotation_id) pairs unique", len({(m["frame_id"], m["annotation_id"]) for m in marks}) == len(marks))
check("all frames reviewed", all(r["reviewed"] == "1" for r in status.values()))
for t, col in (("point", "num_points"), ("box", "num_boxes")):
    per = {}
    for m in marks:
        if m["annotation_type"] == t:
            per[m["frame_id"]] = per.get(m["frame_id"], 0) + 1
    check(f"frame_status {col} matches marks.csv", all(int(r[col]) == per.get(f, 0) for f, r in status.items()))
check("tool backup equals marks.csv (id and class)",
      {(f, m["id"], m["category"]) for f, v in backup.items() for m in v["marks"]}
      == {(m["frame_id"], m["annotation_id"], m["class_label"]) for m in marks})
present = {}
for m in marks:
    present.setdefault(m["frame_id"], set()).add(m["class_label"])
check("presence labels derive from marks.csv",
      all(int(presence[f][c]) == int(c in present.get(f, set())) for f in presence for c in CLASSES))
check("R1 sequence indices and DriveAgent files unique",
      len({r["r1_sequence_index"] for r in index.values()}) == len({r["driveagent_file"] for r in index.values()}) == 300)
check("every frame has a DriveAgent checksum", all(r["driveagent_file"] in sums for r in index.values()))

print(f"{sum(checks)}/{len(checks)} checks passed; {len(marks)} marks on {len(status)} frames")
sys.exit(0 if all(checks) else 1)
