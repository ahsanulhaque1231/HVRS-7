# Datasheet for HVRS-7

Following *Datasheets for Datasets* (Gebru *et al.*, Communications of the ACM, 2021).

## Motivation
- **Purpose.** To provide human-verified, spatially marked object-presence labels for frames of a public driving dataset, so that road-scene recognition, including pedestrians, can be evaluated against labels checked frame by frame, and so that the image region a model relies on can be checked against human marks.
- **Creators.** Ahsanul Haque, Tasnim Sultana Sintheia, Khandaker Tabin Hasan, and M. Shamim Kaiser.

## Composition
- **Instances.** 300 forward-camera frames of DriveAgent Route R1, each with zero or more marks per class over seven classes; 2,213 marks in total (1,729 points, 484 boxes).
- **Sampling.** 300 of the 1,661 R1 frames, spanning sequence indices 3 to 1,660, including the 100 frames for which DriveAgent releases frame labels and 200 further frames. Consecutive annotated frames are 1 to 12 route frames apart (median 5).
- **Labels.** Points and boxes with a class key; frame-level reviewed and unclear flags; a free-text note for 23 of the 24 unclear frames; derived 0/1 presence labels.
- **Missing information.** Not every instance is marked; marks establish presence and location only. No instance identities, tracks, occlusion levels or attributes.
- **Relationships.** Frames are linked to DriveAgent by file name and R1 sequence index (`annotations/frame_index.csv`).
- **Splits.** None are prescribed. Because the frames come from one continuous drive, temporally blocked or route-segment splits are recommended.
- **Noise.** One annotator; inter-annotator agreement not measured. 24 frames are flagged unclear.
- **External resources.** The images come from the DriveAgent release on Hugging Face (`Parechan/driveagent`, revision `5dfff082e289cbe4729ce9960d90b7281c0eb4d3`) and are not redistributed. SHA-256 checksums allow exact verification.
- **Confidential or sensitive data.** None is added by HVRS-7. The source frames are public street scenes that may show people and vehicles; HVRS-7 adds no identity, licence-plate or personal information.

## Collection process
- **Acquisition.** Frames were downloaded from the public DriveAgent release.
- **Annotation.** Manual, by one of the authors, in an offline browser tool with no model, detector or network service (see `docs/ANNOTATION_PROTOCOL.md`). The final file was exported on 18 October 2026.
- **Blinding.** The annotator saw no model output and no released DriveAgent label while marking.

## Preprocessing, cleaning, labelling
- No image preprocessing is applied to the released data. Coordinates refer to the original 2448 × 2048 frames.
- Frame-level presence labels are derived deterministically from the marks.

## Uses
- **Intended.** Evaluation of frame-level multi-label road-scene recognition; localization checks of model evidence against human marks; auditing other labels for these frames.
- **Not intended.** Training or scoring object detectors (marks are not exhaustive); safety certification; any use that attempts to identify people.
- **Caution.** One route and one annotator; small pedestrian sample (45 frames, five episodes).

## Distribution
- **Where.** https://github.com/ahsanulhaque1231/HVRS-7
- **License.** Annotations CC BY 4.0; code MIT. Images under the DriveAgent terms.

## Maintenance
- **Maintainer.** The authors, through the GitHub issue tracker.
- **Updates.** Versioned releases recorded in `CHANGELOG.md`; corrections will be released as new versions without changing existing ones.
- **Contributions.** Additional annotations (for example, a second annotator) are welcome through issues or pull requests.
