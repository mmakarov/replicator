# Contributing to Replicator

Thanks for taking the time to improve Replicator. This document describes how to
set up the project locally and how to propose changes.

## Prerequisites

- Python 3.9 or newer.
- [ffmpeg](https://ffmpeg.org/) and `ffprobe` available on `PATH` (or placed in
  a local `bin/` folder).
- No extra Python packages are required to render from the CLI.

The GUI additionally needs Qt for Python:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install PySide6-Essentials
```

> `requirements.txt` belongs to the legacy MoviePy scripts
> (`source-to-fin.py`, `source-to-fin-win.py`) and is **not** used by the
> current `replicator.py` / `gui_qt.py` path.

## Getting the source

```bash
git clone https://github.com/mmakarov/replicator.git
cd replicator
```

Drop your own `video/source*.mp4`, `audio/voice.mp3`, and `overlay.png` next to
the scripts, or use the sample files shipped in the repository.

## Running locally

GUI:

```bash
python3 gui_qt.py
```

CLI:

```bash
python3 replicator.py \
  --heading "#EVENT" \
  --name "Jane Doe" \
  --extra "United Kingdom" \
  --date "2026-06-19" \
  --audio audio/voice.mp3 \
  --overlay overlay.png \
  --video video/source1.mp4 \
  --video video/source2.mp4
```

A GUI smoke test that does not open a window:

```bash
python3 launcher.py --smoke
```

## Project layout

| Path | Purpose |
| --- | --- |
| `replicator.py` | Rendering pipeline and CLI. |
| `gui_qt.py` | PySide6 desktop interface. |
| `launcher.py` | Self-contained Windows entry point and error logging. |
| `run-windows.bat` | Starts the portable Windows package. |
| `source-to-fin*.py` | Legacy MoviePy scripts, kept for reference. |
| `.github/workflows/` | Windows build/release and smoke-test workflows. |
| `docs/` | Screenshots and supporting documentation. |

## Making changes

- Create a topic branch, for example `fix/free-space-check` or
  `docs/readme-badges`.
- Keep commits focused and use short, imperative messages
  (`Fix Cyrillic drawtext on Windows`).
- Match the existing code style. Do not reformat unrelated code in the same
  change.
- Keep existing user-facing wording consistent across the GUI and CLI.
- If you can, run the optional quality gates:

  ```bash
  ruff check replicator.py gui_qt.py launcher.py
  mypy
  ```

## Pull requests

1. Describe what changed and why.
2. Mention how you tested it (OS, command, and observed result).
3. If the change affects the Windows package, note whether the
   `Build Windows release` workflow passes.

## Reporting issues

Open an issue using the repository issue tracker. Include your operating
system, the exact command, the full log (`render.log` / `startup.log` when
available), and what you expected to happen.

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
