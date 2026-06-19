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

## Windows release smoke test

The GitHub Actions workflow `Windows build and smoke` builds and tests the portable Windows zip on a real Windows runner. It uploads the ready `Replicator-Windows.zip` as an artifact.

1. Open GitHub Actions.
2. Choose `Windows build and smoke`.
3. Click `Run workflow`.
4. Download the `Replicator-Windows` artifact when the run passes.

The workflow downloads embedded Python, PySide6 and ffmpeg, builds the archive, starts `run-windows.bat` in GUI smoke mode, renders a sample `youtube_ready.mp4`, checks the result with ffprobe, and uploads logs/output as artifacts.

The GitHub Actions workflow `Windows release smoke` tests an already published portable Windows zip by URL.

1. Open GitHub Actions.
2. Choose `Windows release smoke`.
3. Click `Run workflow`.
4. Keep the default URL for the latest release, or paste a specific `Replicator-Windows.zip` URL.

The workflow unpacks the archive, starts `run-windows.bat` in GUI smoke mode, renders a sample `youtube_ready.mp4`, checks the result with ffprobe, and uploads logs/output as artifacts.

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
