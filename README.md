# HVRS-7: Human-Verified Road-Scene Marks for DriveAgent Route R1

[![Annotations: CC BY 4.0](https://img.shields.io/badge/annotations-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](CHANGELOG.md)

**HVRS-7** (**H**uman-**V**erified **R**oad-**S**cene marks, **7** classes) is a set of human point and bounding-box annotations for **300 frames of Route R1** of the public **DriveAgent** dataset ([Hugging Face: `Parechan/driveagent`](https://huggingface.co/datasets/Parechan/driveagent); Hou *et al.*, *IEEE Robotics and Automation Letters*, 2025). The 300 frames were selected from Route R1 and annotated for a research study on road-scene recognition with vision–language models.

Every frame was inspected by a human annotator, who marked each class present in it with a point or a box. The set covers **seven road-scene classes, including pedestrians**, which the labels released with DriveAgent do not include. Each frame has a review flag, and frames containing objects that could not be identified are flagged as *unclear* with a free-text note.

This repository releases the **annotations, the frame index linking every annotated frame to its DriveAgent source file, checksums, the offline annotation tool, and scripts** to download the frames, validate the files, and derive frame-level labels. The DriveAgent images themselves are **not** redistributed; `scripts/fetch_frames.py` downloads them from the DriveAgent release and verifies them.

---

## Contents
- [Why HVRS-7](#why-hvrs-7)
- [Source data](#source-data)
- [Dataset at a glance](#dataset-at-a-glance)
- [Class definitions](#class-definitions)
- [Annotation process and quality control](#annotation-process-and-quality-control)
- [Repository structure](#repository-structure)
- [File formats](#file-formats)
- [Getting started](#getting-started)
- [Recommended use](#recommended-use)
- [Limitations](#limitations)
- [Citation](#citation)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Why HVRS-7
- **Human-verified ground truth for a public driving dataset.** DriveAgent provides driving routes with forward-camera frames, GNSS/IMU records and object information for multi-agent driving research. HVRS-7 adds human-verified object-presence labels for 300 forward-camera frames of Route R1, so that perception results on these frames can be scored against labels checked frame by frame.
- **Pedestrians and seven classes.** The marks cover pedestrians, four-wheel vehicles, non-four-wheel vehicles (two- and three-wheelers), signs, monitors (traffic cameras and electronic displays), fixed installations and plants.
- **Spatial evidence, not only frame labels.** Each class presence is marked by a point or box on the object, so the set supports both frame-level recognition and checks of *where* a model locates its evidence (for example, pointing-game style localization).
- **Transparent uncertainty.** Frames with objects that could not be identified are flagged and described, rather than silently dropped or guessed.
- **Reproducible.** Frames are identified by their DriveAgent file name and R1 sequence index, pinned to a fixed revision of the DriveAgent release and verified by SHA-256 checksums.

## Source data
| | |
|---|---|
| Dataset | DriveAgent (Hou *et al.*, 2025) |
| Host | Hugging Face, [`Parechan/driveagent`](https://huggingface.co/datasets/Parechan/driveagent) |
| Revision used | `5dfff082e289cbe4729ce9960d90b7281c0eb4d3` |
| Route | R1, forward camera (`R1/pic_sort/`), 1,661 frames of 2448 × 2048 px at about 10 frames per second (about 166 s of driving) |
| License of the source | MIT, as stated on the Hugging Face dataset card |

HVRS-7 covers 300 of the 1,661 R1 frames, spanning sequence indices 3 to 1,660. Consecutive annotated frames are 1 to 12 route frames apart (median 5, about 0.5 s). The selection includes the 100 frames for which DriveAgent releases frame labels and 200 further frames.

Please cite DriveAgent whenever you use HVRS-7 (see [Citation](#citation)).

## Dataset at a glance
| | |
|---|---|
| Frames | 300 (all reviewed) |
| Marks | 2,213 (1,729 points, 484 boxes) |
| Classes | 7 |
| Mean classes per frame | 4.26 |
| Frames flagged *unclear* | 24 (23 with a note), kept in the set |
| Marks flagged *uncertain* | 0 |
| Annotators | 1 |

| Class | Frames | % of frames | Points | Boxes |
|---|---:|---:|---:|---:|
| Pedestrian | 45 | 15.0 | 25 | 54 |
| Four-wheel vehicle | 174 | 58.0 | 207 | 61 |
| Non-four-wheel vehicle | 212 | 70.7 | 50 | 200 |
| Sign | 127 | 42.3 | 92 | 130 |
| Monitor | 120 | 40.0 | 187 | 30 |
| Fixed installation | 299 | 99.7 | 824 | 9 |
| Plant | 300 | 100.0 | 344 | 0 |
| **Total** | 300 | – | **1,729** | **484** |

## Class definitions
| Key | Class | Definition |
|---|---|---|
| `pedestrian` | Pedestrian | A person on foot who is not riding (walking, standing, waiting or working), including small and distant people. Riders of any two- or three-wheeler are **not** pedestrians. |
| `four_wheel_vehicle` | Four-wheel vehicle | A car, van, SUV, truck, trailer or bus, moving or parked. |
| `non_four_wheel_vehicle` | Non-four-wheel vehicle | A bicycle, e-bike, scooter, motorcycle or tricycle, with or without a rider. |
| `sign` | Sign | An official traffic sign or road signboard. Shop names and traffic lights do not count. |
| `fixed_installation` | Fixed installation | A building, wall, fence, guardrail, barrier, pole, lamp post, gantry or bridge. |
| `plant` | Plant | A tree, shrub, hedge or grass verge. |
| `monitor` | Monitor | A traffic-supervision camera on a pole, arm or gantry, or an electronic display, message board or countdown display. |

A class is **present** in a frame if the frame has at least one mark of that class. See [`docs/ANNOTATION_PROTOCOL.md`](docs/ANNOTATION_PROTOCOL.md) for the full protocol.

## Annotation process and quality control
- **Annotator.** One of the authors annotated all 300 frames; the final annotation file was exported on 18 October 2026.
- **Tool.** An offline browser tool (*R1 Visual Label Studio*, in [`tool/`](tool/)) that runs no model, detector or network service. Every mark was created by the annotator; nothing was pre-filled.
- **Blind to other labels.** The annotator saw no released DriveAgent label or model output while marking. The released labels were compared only after all 300 frames were complete.
- **Marks.** Each mark is a point or a box, at the annotator's choice. Marks establish *presence* and *location*; not every instance in a frame is necessarily marked.
- **Frame review.** Every frame was marked *reviewed* after inspection. Frames with objects that could not be resolved (mostly distant road users and partly occluded objects) were flagged *unclear* and described in a note.
- **Reference panel.** For the first 32 frames (F001–F032), the tool showed earlier frame-level presence flags from a manual check in a collapsible, read-only panel. These flags create no marks, and the final labels differ from them in 22 of 224 frame–class cells.
- **Consistency checks.** `scripts/validate.py` runs 13 checks (counts, classes, coordinates, consistency between files, frame index, checksums). All pass for version 1.0.0.

A datasheet following *Datasheets for Datasets* (Gebru *et al.*, 2021) is in [`docs/DATASHEET.md`](docs/DATASHEET.md).

## Repository structure
```
HVRS-7/
├── annotations/
│   ├── marks.csv              one row per mark (2,213 rows)
│   ├── frame_status.csv       one row per frame (300 rows): reviewed, unclear, counts, note
│   ├── frame_index.csv        frame_id -> R1 sequence index and DriveAgent file
│   └── tool_backup.json       the same marks in the annotation tool's re-importable format
├── derived/
│   └── presence_labels.csv    300 × 7 frame-level presence labels (0/1) derived from marks.csv
├── checksums/
│   └── driveagent_r1_sha256.txt   SHA-256 of the 300 DriveAgent source frames
├── scripts/
│   ├── fetch_frames.py        download and verify the 300 frames from DriveAgent
│   ├── validate.py            consistency checks (all must pass)
│   ├── make_presence_labels.py   rebuild derived/presence_labels.csv
│   └── visualize.py           draw the marks of one frame
├── tool/                      offline annotation tool (open tool/index.html)
├── docs/
│   ├── ANNOTATION_PROTOCOL.md
│   └── DATASHEET.md
├── CITATION.cff
├── CHANGELOG.md
└── LICENSE
```

## File formats
### `annotations/marks.csv`
| Column | Meaning |
|---|---|
| `frame_id` | `F001`–`F300` |
| `annotation_id` | mark id, unique within its frame (the pair `frame_id`, `annotation_id` is unique) |
| `annotation_type` | `point` or `box` |
| `class_label` | one of the seven class keys |
| `uncertain` | per-mark uncertainty flag (0 for every mark in v1.0.0) |
| `x_norm`, `y_norm` | point position, or box top-left corner, as a fraction of image width and height |
| `width_norm`, `height_norm` | box width and height as a fraction of the image (empty for points) |
| `x_px`, `y_px`, `width_px`, `height_px` | the same in pixels of the 2448 × 2048 original |
| `frame_reviewed`, `frame_unclear`, `frame_note` | the frame-level status, repeated on each row for convenience |

### `annotations/frame_status.csv`
`frame_id`, `reviewed` (0/1), `unclear` (0/1), `num_points`, `num_boxes`, `note`.

### `annotations/frame_index.csv`
`frame_id`, `r1_sequence_index` (0-based position of the frame in R1 ordered by capture timestamp), `driveagent_file` (path in the DriveAgent repository, for example `R1/pic_sort/1726283916665923985.jpg`).

### `derived/presence_labels.csv`
`frame_id` followed by one 0/1 column per class; a class is 1 when the frame has at least one mark of it.

### `annotations/tool_backup.json`
The full annotation state in the tool's format (`r1-manual-visual-labels-v1`). Import it in the tool to view or extend the marks.

## Getting started
Requirements: Python 3.8 or later. The download and validation scripts use only the standard library; `visualize.py` needs Pillow.

```bash
git clone https://github.com/ahsanulhaque1231/HVRS-7.git
cd HVRS-7

python scripts/validate.py                    # 13/13 checks should pass
python scripts/fetch_frames.py                # downloads images/F001.jpg ... F300.jpg (about 200 MB) and verifies them
python scripts/visualize.py F191              # writes F191_marks.png
```

Load the labels in Python:
```python
import pandas as pd

marks = pd.read_csv("annotations/marks.csv")
labels = pd.read_csv("derived/presence_labels.csv", index_col="frame_id")
index = pd.read_csv("annotations/frame_index.csv", index_col="frame_id")

print(labels.mean().round(3))                          # class frequencies
print(marks.query("frame_id == 'F191'")[["annotation_type", "class_label", "x_px", "y_px"]])
```

To view or edit the marks in the annotation tool, run `python scripts/fetch_frames.py --out tool/images`, open `tool/index.html` in a recent browser, and import `annotations/tool_backup.json` (see [`tool/TOOL_GUIDE.md`](tool/TOOL_GUIDE.md)).

## Recommended use
- **Frame-level recognition.** Use `derived/presence_labels.csv` as ground truth for multi-label recognition of the seven classes.
- **Localization checks.** Use the marks to test whether the image region a model points to contains the object (a hit when the region contains a mark of the class).
- **Label auditing.** Compare other labels for these frames, including those released with DriveAgent, against the human marks.
- **Mind temporal correlation.** The frames come from one continuous drive of about 166 s, so neighbouring frames are near-duplicates. Use temporally blocked or route-segment splits with a guard band, never random frame-level splits, and report uncertainty with resampling over time blocks rather than frames.
- **Unclear frames.** Keep them in evaluation; optionally report results with and without them.

## Limitations
- One annotator; inter-annotator agreement has not been measured.
- One route of about 166 s; results may not transfer to other routes, cities, weather or lighting.
- Pedestrians appear in only 45 frames from five episodes.
- Marks establish class presence and location but are not an exhaustive instance-level annotation; HVRS-7 is not a detection benchmark.
- Fixed installations and plants are present in almost every frame, so they carry little information for frame-level evaluation.

## Citation
HVRS-7 accompanies a journal article that is currently under review; its reference will be added here on publication. Until then, please cite the dataset and the DriveAgent source:

```bibtex
@misc{hvrs7_2026,
  author       = {Haque, Ahsanul and Sintheia, Tasnim Sultana and Hasan, Khandaker Tabin and Kaiser, M. Shamim},
  title        = {{HVRS-7}: Human-Verified Road-Scene Marks for {DriveAgent} Route {R1}},
  year         = {2026},
  version      = {1.0.0},
  howpublished = {GitHub repository},
  url          = {https://github.com/ahsanulhaque1231/HVRS-7}
}

@article{hou2025driveagent,
  author  = {Hou, X. and others},
  title   = {{DriveAgent}: Multi-Agent Structured Reasoning With {LLM} and Multimodal Sensor Fusion for Autonomous Driving},
  journal = {IEEE Robotics and Automation Letters},
  year    = {2025},
  doi     = {10.1109/LRA.2025.3619807}
}

@misc{driveagent_dataset,
  author       = {Hou, X. and others},
  title        = {{DriveAgent} Dataset},
  year         = {2025},
  howpublished = {Hugging Face},
  url          = {https://huggingface.co/datasets/Parechan/driveagent}
}
```
GitHub also offers a citation for this repository through [`CITATION.cff`](CITATION.cff) ("Cite this repository").

## License
- **Annotations** (`annotations/`, `derived/`, `checksums/`, `docs/`): [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- **Code** (`scripts/`, `tool/`): MIT License.
- **Images:** not included. The DriveAgent frames remain subject to the terms of the DriveAgent release (MIT, per its Hugging Face dataset card) and must be obtained from it.

See [`LICENSE`](LICENSE).

## Acknowledgments
We thank the DriveAgent authors for releasing their dataset publicly on Hugging Face; HVRS-7 would not exist without it.

Questions and corrections are welcome through the [issue tracker](https://github.com/ahsanulhaque1231/HVRS-7/issues).
