# R1 Visual Label Studio (offline annotation tool)

The tool used to create HVRS-7. It runs entirely in the browser from local files: no installation, account, network connection, model or server.

## Setup
1. From the repository root, download the frames into the tool folder:
   `python scripts/fetch_frames.py --out tool/images`
2. Open `tool/index.html` in a recent Chrome, Chromium, Edge or Firefox.
3. To load the released marks, choose **Import** and select `annotations/tool_backup.json`.

## Labelling
- **Point mode** (default): click an object and choose one of the seven classes. Click a point to change its class or delete it; drag it to move it.
- **Box mode:** drag a rectangle over an object, then choose its class. Click or drag a box to edit or move it. Shift+drag starts a new box inside an existing one.
- Mark a frame **Reviewed** after checking it, including frames without foreground objects. Use **Unclear** when an object cannot be identified, and describe it in the note.
- For F001–F032, a collapsible read-only panel shows earlier frame-level presence flags. It never creates marks.

## Export
- **Backup (.json):** full state, re-importable.
- **Annotation table (.csv):** one row per mark, with normalized and pixel coordinates.
- **Frame status (.csv):** review state and counts for all frames.
- **Annotated image (.jpg) / all reviewed images (.zip):** copies with marks drawn; source images are never modified.

Browser storage is temporary; export the JSON backup regularly.

## Shortcuts
| Key | Action |
|---|---|
| 1–7 (menu open) | assign class |
| Q / B | point / box mode |
| N / P or → / ← | next / previous frame |
| R | toggle reviewed |
| + / − / 0 | zoom in / out / fit |
| Wheel | zoom at cursor |
| Space+drag or middle-drag | pan |
| Ctrl+Z / Ctrl+Y | undo / redo |
| Esc | close menu |
