# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- MIT license.
- Community health files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, and this changelog.
- `pyproject.toml` with project metadata and `ruff` / `mypy` configuration.
- `.editorconfig` for consistent formatting across editors.
- GUI screenshot in `docs/`.

### Changed

- Rewrote `README.md` with badges, screenshot, project structure, and
  troubleshooting.

### Documentation

- Clarified the legacy status of `source-to-fin.py`, `source-to-fin-win.py`, and
  `requirements.txt`.

## [7] - 2026-06-24

### Fixed

- Cyrillic text rendering in `drawtext` on Windows.

## [6] - 2026-06-19

### Fixed

- Include the application root in the embedded Python path so the portable
  Windows package can import local modules.

## [5] - 2026-06-19

### Changed

- Made the GitHub Windows smoke test headless.
- Improved launcher startup diagnostics.

## [4] - 2026-06-19

### Added

- `startup.log` and `render.log` diagnostics.
- Windows release smoke workflow.

### Fixed

- Windows launcher startup.

## [3] - 2026-05-24

### Added

- First GUI release with a Windows/macOS interface.
- Portable, self-contained Windows build (embedded Python, Qt, and ffmpeg).

## [0.1.0] - 2020-08-06

### Added

- Initial MoviePy-based script that merges source videos, a transparent PNG
  overlay, text areas, and an MP3 audio track into `youtube_ready.mp4`.

[Unreleased]: https://github.com/mmakarov/replicator/compare/v7...HEAD
[7]: https://github.com/mmakarov/replicator/compare/v6...v7
[6]: https://github.com/mmakarov/replicator/compare/v5...v6
[5]: https://github.com/mmakarov/replicator/compare/v4...v5
[4]: https://github.com/mmakarov/replicator/compare/v3...v4
[3]: https://github.com/mmakarov/replicator/releases/tag/v3
[0.1.0]: https://github.com/mmakarov/replicator/commit/57654b1
