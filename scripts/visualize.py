"""Draw the HVRS-7 marks of one frame on its image.
Requires Pillow (pip install pillow) and the frames from scripts/fetch_frames.py.
Usage: python scripts/visualize.py F191 [--images images] [--out F191_marks.png]"""
import argparse
import csv
from PIL import Image, ImageDraw, ImageFont

COLORS = {"pedestrian": (230, 25, 75), "four_wheel_vehicle": (0, 130, 200),
          "non_four_wheel_vehicle": (245, 130, 48), "sign": (255, 225, 25),
          "fixed_installation": (145, 30, 180), "plant": (60, 180, 75), "monitor": (70, 240, 240)}

ap = argparse.ArgumentParser()
ap.add_argument("frame_id")
ap.add_argument("--images", default="images")
ap.add_argument("--out")
a = ap.parse_args()

img = Image.open(f"{a.images}/{a.frame_id}.jpg").convert("RGB")
d = ImageDraw.Draw(img)
try:
    font = ImageFont.load_default(size=40)  # Pillow >= 10.1
except TypeError:
    font = ImageFont.load_default()
for m in csv.DictReader(open("annotations/marks.csv", newline="")):
    if m["frame_id"] != a.frame_id:
        continue
    c = COLORS[m["class_label"]]
    x, y = float(m["x_px"]), float(m["y_px"])
    if m["annotation_type"] == "box":
        d.rectangle([x, y, x + float(m["width_px"]), y + float(m["height_px"])], outline=c, width=5)
    else:
        d.ellipse([x - 14, y - 14, x + 14, y + 14], outline=c, width=6)
    d.text((x + 16, y - 48), m["class_label"], fill=c, font=font)
out = a.out or f"{a.frame_id}_marks.png"
img.save(out)
print("wrote", out)
