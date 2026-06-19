# Replicator

Replicator creates a YouTube-ready video from:

- one or more source videos;
- one audio track;
- a transparent PNG overlay;
- four short text fields.

The final `youtube_ready.mp4` is automatically looped to match the audio length.

## Windows: easiest way

Download the latest release archive from GitHub Releases:

`Replicator-Windows.zip`

Then:

1. Unzip it anywhere.
2. Double-click `run-windows.bat`.
3. Choose video files, one audio file, and optionally another PNG overlay.
4. Click `Старт`.
5. The result will appear next to the app as `youtube_ready.mp4`.

Nothing else needs to be installed. The release archive already includes Python, Qt, ffmpeg, fonts, and sample files.

## Default files

The Windows package includes sample inputs:

- `video/source1.mp4`
- `video/source2.mp4`
- `video/source4.mp4`
- `audio/voice.mp3`
- `overlay.png`

The overlay from the package is selected by default on startup.

## Current GUI behavior

- UI language is Russian.
- Multiple video files can be selected from anywhere on disk.
- Audio and overlay are selected by path; the app does not delete or overwrite selected source files.
- Before rendering, the app checks free disk space and shows an error if there is not enough room.
- ffmpeg progress is streamed into the log so long renders do not look frozen.
- Startup/render failures are written to `startup.log` and `render.log` next to `run-windows.bat`.

## Windows release workflow

The GitHub Actions workflow `Build Windows release` builds, smoke-tests, and publishes a self-contained Windows release.

1. Open GitHub Actions.
2. Choose `Build Windows release`.
3. Click `Run workflow`.
4. Enter a new version tag, for example `v6`.

The workflow runs on `windows-latest`, downloads embedded Python, PySide6 Essentials, shiboken6 and ffmpeg during the build, creates `dist/Replicator-Windows.zip`, runs the Windows smoke tests against the built package, and only then creates the GitHub Release.

The separate workflow `Windows release smoke` can still test an already published `Replicator-Windows.zip` by URL.

## Developer run

On macOS/Linux with ffmpeg installed:

```bash
python3 replicator.py \
  --heading Test \
  --name Name \
  --extra Country \
  --date Date \
  --audio audio/voice.mp3 \
  --overlay overlay.png \
  --video video/source1.mp4 \
  --video video/source2.mp4
```

The legacy scripts are kept for reference:

- `source-to-fin.py`
- `source-to-fin-win.py`
