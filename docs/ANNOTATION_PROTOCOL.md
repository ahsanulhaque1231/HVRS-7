# HVRS-7 annotation protocol

This document describes how the HVRS-7 marks were made, so that the set can be interpreted, extended, or re-annotated consistently.

## 1. Task
For each of the 300 DriveAgent Route R1 frames, mark every one of the seven classes that is visible in the frame with at least one point or box placed on an instance of the class. A class with no mark is treated as absent.

## 2. Classes
| # | Key | Include | Exclude |
|---|---|---|---|
| 1 | `pedestrian` | A person on foot who is not riding: walking, standing, waiting or working; small and distant people | Riders of bicycles, scooters, motorcycles or tricycles |
| 2 | `four_wheel_vehicle` | Car, van, SUV, truck, trailer, bus; moving or parked | – |
| 3 | `non_four_wheel_vehicle` | Bicycle, e-bike, scooter, motorcycle, tricycle; with or without a rider | – |
| 4 | `sign` | Official traffic sign or road signboard | Shop names, advertising, traffic lights |
| 5 | `fixed_installation` | Building, wall, fence, guardrail, barrier, pole, lamp post, gantry, bridge | – |
| 6 | `plant` | Tree, shrub, hedge, grass verge | – |
| 7 | `monitor` | Traffic-supervision camera on a pole, arm or gantry; electronic display, message board, countdown display | – |

## 3. Mark types
- **Point:** a click on the object, recorded as normalized and pixel coordinates.
- **Box:** a rectangle drawn around the object, recorded by its top-left corner, width and height.

Points and boxes have the same meaning for presence. Boxes are not guaranteed to be tight or to cover every instance, so the marks should not be used to train or score object detectors.

## 4. Frame-level flags
- **Reviewed:** set after the whole frame was inspected, including frames where only background classes are present. All 300 frames are reviewed.
- **Unclear:** set when an object in the frame could not be assigned to a class with confidence (for example, blurred distant road users or occluded objects behind a fence). A free-text note describes the location and the reason. Unclear frames remain in the set; their confident marks are kept.
- **Uncertain (per mark):** available in the tool; not used in v1.0.0.

## 5. Procedure
1. The annotator opened each frame at its original resolution (2448 × 2048) in the offline tool, with zoom and pan.
2. Classes were marked from the definitions above. No model output, detector box, or released DriveAgent label was shown.
3. For F001–F032 only, a read-only panel listed earlier frame-level presence flags from a manual check. The panel never created marks; the final labels differ from it in 22 of 224 frame–class cells.
4. Each frame was flagged *reviewed* and, where needed, *unclear* with a note.
5. The final state was exported from the tool (`annotations/tool_backup.json`, `annotations/marks.csv`, `annotations/frame_status.csv`).
6. The exports were checked with `scripts/validate.py`.

## 6. Deriving frame labels
`scripts/make_presence_labels.py` sets class *c* of a frame to 1 when the frame has at least one mark of *c*, and to 0 otherwise. The result is `derived/presence_labels.csv`.
