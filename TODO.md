# TODO

Notes for later iterations. Do not change the working release path just for cleanup.

## Packaging and release

- Pin downloadable build inputs in `Build Windows release` more strictly:
  embedded Python version, PySide6 version, shiboken6 version, ffmpeg build URL.
- Add SHA256 checks for downloaded Python, PySide6/shiboken6 wheels, and ffmpeg archive.
- Keep the user-facing `Replicator-Windows.zip` fully self-contained. Downloads are allowed only inside GitHub Actions during release build.

## Project cleanup

- Move or remove legacy MoviePy scripts: `source-to-fin.py` and `source-to-fin-win.py`.
- Update or remove old `requirements.txt`; the current Windows release path does not use MoviePy/numpy/audioread.
- Clarify old `README.txt` versus current `README.md` / `WINDOWS_README.txt`.
- Add `pyproject.toml` with project-specific `ruff` rules so linting ignores intentional Russian UI strings and legacy files if they stay.

## Converter robustness

- Avoid overwriting `youtube_ready.mp4` silently. Prefer timestamped output names or a GUI confirmation before overwrite.
- Replace module-level mutable globals in `replicator.py` with an explicit render config object.
- Improve free-space estimation using audio duration and expected output/intermediate bitrate instead of only selected input size.

## Quality gates

- Keep `ruff check replicator.py gui_qt.py launcher.py` and `mypy --ignore-missing-imports --follow-imports=skip replicator.py gui_qt.py launcher.py` green.
- Consider formatting `replicator.py` and `gui_qt.py` with `ruff format` in a separate low-risk cleanup commit.
- Tune `yamllint` rules for GitHub Actions workflows or add an Actions-aware linter.
