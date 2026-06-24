#!/usr/bin/env python
import math
import os
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


for stream_name in ("stdin", "stdout", "stderr"):
    stream = getattr(sys, stream_name)
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "video"
DEFAULT_AUDIO_FILE = ROOT / "audio" / "voice.mp3"
DEFAULT_OVERLAY_FILE = ROOT / "overlay.png"
AUDIO_FILE = DEFAULT_AUDIO_FILE
OVERLAY_FILE = DEFAULT_OVERLAY_FILE
MEDIUM_FILE = ROOT / "medium.mp4"
SILENT_FILE = ROOT / "silent_fin.mp4"
FINAL_FILE = ROOT / "youtube_ready.mp4"
MAX_TEXT_LENGTH = 20
PAUSE_ON_ERROR = True
TEXT_FILE_NAMES = {
    "heading": "drawtext_heading.txt",
    "name": "drawtext_name.txt",
    "extra": "drawtext_extra.txt",
    "date": "drawtext_date.txt",
}


def natural_key(path):
    parts = []
    current = ""
    is_digit = False
    for char in path.name.lower():
        if char.isdigit() != is_digit:
            if current:
                parts.append(int(current) if is_digit else current)
            current = char
            is_digit = char.isdigit()
        else:
            current += char
    if current:
        parts.append(int(current) if is_digit else current)
    return parts


def app_path(*parts):
    return ROOT.joinpath(*parts)


def ffmpeg_path():
    local = app_path("bin", "ffmpeg.exe")
    if local.exists():
        return str(local)
    local_unix = app_path("bin", "ffmpeg")
    if local_unix.exists():
        return str(local_unix)
    found = shutil.which("ffmpeg")
    if found:
        return found
    fail("Не найден ffmpeg. В переносной Windows-сборке он должен лежать в папке bin.")


def ffprobe_path():
    local = app_path("bin", "ffprobe.exe")
    if local.exists():
        return str(local)
    local_unix = app_path("bin", "ffprobe")
    if local_unix.exists():
        return str(local_unix)
    found = shutil.which("ffprobe")
    if found:
        return found
    fail("Не найден ffprobe. В переносной Windows-сборке он должен лежать в папке bin.")


def fail(message):
    print("")
    print("ОШИБКА: " + message)
    print("")
    if PAUSE_ON_ERROR:
        input("Нажмите Enter, чтобы закрыть окно...")
    sys.exit(1)


def prompt_text(label, default):
    value = input(f"{label} ({MAX_TEXT_LENGTH} зн., Enter = {default}): ").strip()
    if not value:
        return default
    if len(value) > MAX_TEXT_LENGTH:
        fail(f"Слишком длинный текст: {label}")
    return value


def validate_text(label, value, default):
    value = (value or "").strip()
    if not value:
        return default
    if len(value) > MAX_TEXT_LENGTH:
        fail(f"Слишком длинный текст: {label}")
    return value


def run(command):
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    assert process.stdout is not None
    pending = ""
    for chunk in iter(lambda: process.stdout.read(1), ""):
        if chunk == "\r":
            if pending.strip():
                print(pending.strip(), flush=True)
            pending = ""
        elif chunk == "\n":
            if pending.strip():
                print(pending.strip(), flush=True)
            pending = ""
        else:
            pending += chunk
    if pending.strip():
        print(pending.strip(), flush=True)
    result = process.wait()
    if result != 0:
        fail("ffmpeg завершился с ошибкой. Проверьте входные файлы и попробуйте еще раз.")


def probe_duration(path):
    result = subprocess.run(
        [
            ffprobe_path(),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail(f"Не удалось прочитать длительность файла {path.name}")
    try:
        return float(result.stdout.strip())
    except ValueError:
        fail(f"ffprobe вернул непонятную длительность для файла {path.name}")


def escape_filter_value(value):
    return str(value).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def font_path(bold=False):
    font_name = "NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf"
    bundled = ROOT / "fonts" / font_name
    if bundled.exists():
        return f"fonts/{font_name}"
    if os.name == "nt":
        return "C\\:/Windows/Fonts/arialbd.ttf" if bold else "C\\:/Windows/Fonts/arial.ttf"
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate.replace(":", "\\:")
    return "Arial"


def write_text_files(texts):
    text_files = {}
    for key, file_name in TEXT_FILE_NAMES.items():
        path = ROOT / file_name
        path.write_text(texts[key], encoding="utf-8", errors="replace")
        text_files[key] = file_name
    return text_files


def drawtext(text_file, size, y, bold=False):
    font = escape_filter_value(font_path(bold))
    text_file = escape_filter_value(text_file)
    return (
        "drawtext="
        f"fontfile='{font}':"
        f"textfile='{text_file}':"
        f"fontsize={size}:"
        "fontcolor=white:"
        "x=(w-text_w)/2:"
        f"y={y}"
    )


def collect_sources(selected_sources=None):
    if selected_sources:
        sources = [Path(source) for source in selected_sources]
    else:
        if not VIDEO_DIR.exists():
            fail("Нет папки video.")
        sources = sorted(
            [
                path
                for path in VIDEO_DIR.iterdir()
                if path.is_file()
                and path.suffix.lower() == ".mp4"
                and path.stem.lower().startswith("source")
            ],
            key=natural_key,
        )
    if not sources:
        fail("В папке video нет файлов source1.mp4, source2.mp4 и так далее.")
    missing = [str(source) for source in sources if not source.exists()]
    if missing:
        fail("Не найдены видеофайлы: " + ", ".join(missing))
    return sources


def check_inputs():
    if not AUDIO_FILE.exists():
        fail("Нет аудиофайла: " + str(AUDIO_FILE))
    if not OVERLAY_FILE.exists():
        fail("Нет PNG-оверлея: " + str(OVERLAY_FILE))


def create_medium(sources, texts):
    ffmpeg = ffmpeg_path()
    text_files = write_text_files(texts)
    command = [ffmpeg, "-hide_banner", "-stats", "-y"]
    for source in sources:
        command.extend(["-i", str(source)])
    command.extend(["-i", str(OVERLAY_FILE)])

    filters = []
    scaled_labels = []
    for index, _source in enumerate(sources):
        label = f"v{index}"
        scaled_labels.append(f"[{label}]")
        filters.append(
            f"[{index}:v]scale=1280:720:force_original_aspect_ratio=increase,"
            f"crop=1280:720,setsar=1[{label}]"
        )

    filters.append("".join(scaled_labels) + f"concat=n={len(sources)}:v=1:a=0[base]")
    overlay_index = len(sources)
    filters.append(f"[{overlay_index}:v]scale=1280:720[overlay]")
    filters.append("[base][overlay]overlay=0:0:format=auto[with_overlay]")
    filters.append(
        "[with_overlay]"
        + ",".join(
            [
                drawtext(text_files["heading"], 68, 150),
                drawtext(text_files["name"], 42, 250, bold=True),
                drawtext(text_files["extra"], 42, 300),
                drawtext(text_files["date"], 36, 400),
            ]
        )
        + "[outv]"
    )

    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[outv]",
            "-an",
            "-r",
            "24",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-pix_fmt",
            "yuv420p",
            str(MEDIUM_FILE),
        ]
    )
    run(command)


def create_final():
    ffmpeg = ffmpeg_path()
    audio_duration = probe_duration(AUDIO_FILE)
    video_duration = probe_duration(MEDIUM_FILE)
    audio_length = math.ceil(audio_duration)
    video_length = math.ceil(video_duration)
    if video_length <= 0:
        fail("Промежуточное видео получилось нулевой длины.")

    repeats = max(1, math.ceil(audio_duration / video_duration))
    loop = repeats - 1

    print(f"Длительность аудио: {audio_length} секунд")
    print(f"Длительность видео: {video_length} секунд")
    print(f"Повторов видео: {repeats}")
    print("Сохраняем большое видео без звука...")
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-stats",
            "-y",
            "-stream_loop",
            str(loop),
            "-i",
            str(MEDIUM_FILE),
            "-c",
            "copy",
            str(SILENT_FILE),
        ]
    )

    print("Добавляем звуковую дорожку...")
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-stats",
            "-y",
            "-i",
            str(SILENT_FILE),
            "-i",
            str(AUDIO_FILE),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            str(FINAL_FILE),
        ]
    )


def cleanup():
    temp_text_files = [ROOT / file_name for file_name in TEXT_FILE_NAMES.values()]
    for path in (SILENT_FILE, MEDIUM_FILE, *temp_text_files):
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def parse_args():
    parser = argparse.ArgumentParser(description="Replicator video builder")
    parser.add_argument("--heading", default=None)
    parser.add_argument("--name", default=None)
    parser.add_argument("--extra", default=None)
    parser.add_argument("--date", default=None)
    parser.add_argument("--video", action="append", default=[])
    parser.add_argument("--audio", default=None)
    parser.add_argument("--overlay", default=None)
    parser.add_argument("--no-pause", action="store_true")
    return parser.parse_args()


def main():
    global AUDIO_FILE, OVERLAY_FILE, PAUSE_ON_ERROR
    args = parse_args()
    PAUSE_ON_ERROR = not args.no_pause
    if args.audio:
        AUDIO_FILE = Path(args.audio)
    if args.overlay:
        OVERLAY_FILE = Path(args.overlay)
    os.chdir(ROOT)
    print("Replicator: подготовка видео для YouTube")
    print("")
    check_inputs()
    sources = collect_sources(args.video)
    print("Найдены видео:")
    for source in sources:
        print("  " + source.name)
    print("")

    if any(value is not None for value in (args.heading, args.name, args.extra, args.date)):
        texts = {
            "heading": validate_text("Введите заголовок", args.heading, "#ЗАГОЛОВОК"),
            "name": validate_text("Введите имя", args.name, "Имя"),
            "extra": validate_text("Введите дополнительный текст", args.extra, "Страна"),
            "date": validate_text("Введите дату", args.date, "Дата мероприятия"),
        }
    else:
        texts = {
            "heading": prompt_text("Введите заголовок", "#ЗАГОЛОВОК"),
            "name": prompt_text("Введите имя", "Имя"),
            "extra": prompt_text("Введите дополнительный текст", "Страна"),
            "date": prompt_text("Введите дату", "Дата мероприятия"),
        }

    cleanup()
    print("")
    print("Собираем видео с оверлеем и текстом...")
    create_medium(sources, texts)
    create_final()
    cleanup()
    print("")
    print("Сделано! Готовый файл:")
    print(str(FINAL_FILE))
    print("")
    if PAUSE_ON_ERROR:
        input("Нажмите Enter, чтобы закрыть окно...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print("Остановлено пользователем.")
