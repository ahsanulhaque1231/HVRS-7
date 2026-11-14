# Changelog

## [1.0.0] – 2026-11-14
First public release.
- 300 DriveAgent Route R1 frames, 2,213 marks (1,729 points, 484 boxes), seven classes.
- Frame status with review and unclear flags (24 unclear frames, 23 with notes).
- Frame index linking each frame to its DriveAgent file and R1 sequence index; SHA-256 checksums of the source frames at DriveAgent revision `5dfff082e289cbe4729ce9960d90b7281c0eb4d3`.
- Derived 300 × 7 presence labels.
- Scripts: `fetch_frames.py`, `validate.py` (13 checks), `make_presence_labels.py`, `visualize.py`.
- Offline annotation tool and guide; annotation protocol and datasheet.
