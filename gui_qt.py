#!/usr/bin/env python
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


ROOT = Path(__file__).resolve().parent
MAX_TEXT_LENGTH = 20


class ReplicatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.process = None
        self.video_files = sorted((ROOT / "video").glob("source*.mp4"))
        self.audio_file = ROOT / "audio" / "voice.mp3"
        self.overlay_file = ROOT / "overlay.png"
        self.setWindowTitle("Replicator")
        self.resize(900, 680)
        self.setMinimumSize(780, 580)
        self.build_ui()
        self.refresh_status()

    def build_ui(self):
        self.setStyleSheet(
            """
            QWidget { background: #f6f7f9; color: #171a1f; font-size: 14px; }
            QGroupBox {
                background: white;
                border: 1px solid #d8dde5;
                border-radius: 8px;
                margin-top: 18px;
                padding: 14px;
                font-weight: 700;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }
            QLineEdit, QTextEdit {
                background: white;
                border: 1px solid #c8ced8;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #0b6bcb;
            }
            QPushButton {
                background: white;
                border: 1px solid #c8ced8;
                border-radius: 6px;
                padding: 9px 14px;
                min-height: 18px;
            }
            QPushButton:hover { background: #eef3f8; }
            QPushButton#startButton {
                background: #0b6bcb;
                border-color: #0b6bcb;
                color: white;
                font-weight: 700;
            }
            QPushButton#startButton:hover { background: #084f97; }
            QPushButton:disabled { color: #8b949e; background: #edf0f4; }
            QLabel#title { font-size: 30px; font-weight: 800; }
            QLabel#subtitle { color: #687282; }
            QTextEdit#log { background: #101418; color: #dbe5ef; font-family: Consolas, Menlo, monospace; }
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(22, 20, 22, 22)
        root.setSpacing(14)

        title = QLabel("Replicator")
        title.setObjectName("title")
        subtitle = QLabel("Выберите видео, аудио и оверлей, затем нажмите Старт")
        subtitle.setObjectName("subtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        top = QHBoxLayout()
        top.setSpacing(14)
        root.addLayout(top, 0)

        form_group = QGroupBox("Текст на видео")
        form_layout = QGridLayout(form_group)
        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(10)
        self.heading = self.make_input("#ЗАГОЛОВОК")
        self.name = self.make_input("Имя")
        self.extra = self.make_input("Страна")
        self.date = self.make_input("Дата мероприятия")
        for row, (label, field) in enumerate(
            [
                ("Заголовок", self.heading),
                ("Имя", self.name),
                ("Дополнительный текст", self.extra),
                ("Дата", self.date),
            ]
        ):
            form_layout.addWidget(QLabel(label), row, 0)
            form_layout.addWidget(field, row, 1)
        top.addWidget(form_group, 1)

        files_group = QGroupBox("Файлы")
        files_layout = QVBoxLayout(files_group)
        self.status = QLabel()
        self.status.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.status.setWordWrap(True)
        files_layout.addWidget(self.status, 1)
        file_buttons = QGridLayout()
        self.choose_video_button = QPushButton("Выбрать видео")
        self.choose_video_button.clicked.connect(self.choose_videos)
        self.choose_audio_button = QPushButton("Выбрать аудио")
        self.choose_audio_button.clicked.connect(self.choose_audio)
        self.choose_overlay_button = QPushButton("Выбрать оверлей")
        self.choose_overlay_button.clicked.connect(self.choose_overlay)
        self.refresh_button = QPushButton("Сбросить")
        self.refresh_button.clicked.connect(self.reset_defaults)
        file_buttons.addWidget(self.choose_video_button, 0, 0)
        file_buttons.addWidget(self.choose_audio_button, 0, 1)
        file_buttons.addWidget(self.choose_overlay_button, 1, 0)
        file_buttons.addWidget(self.refresh_button, 1, 1)
        files_layout.addLayout(file_buttons)
        top.addWidget(files_group, 1)

        actions = QHBoxLayout()
        self.start_button = QPushButton("Старт")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_build)
        self.open_button = QPushButton("Открыть результат")
        self.open_button.clicked.connect(self.open_result)
        actions.addWidget(self.start_button)
        actions.addWidget(self.open_button)
        actions.addStretch(1)
        root.addLayout(actions)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #d8dde5;")
        root.addWidget(separator)

        log_group = QGroupBox("Лог")
        log_layout = QVBoxLayout(log_group)
        self.log = QTextEdit()
        self.log.setObjectName("log")
        self.log.setReadOnly(True)
        log_layout.addWidget(self.log)
        root.addWidget(log_group, 1)

    def make_input(self, value):
        field = QLineEdit(value)
        field.setMaxLength(MAX_TEXT_LENGTH)
        return field

    def refresh_status(self):
        videos = [Path(path).name for path in self.video_files]
        lines = [
            "Видео: " + (", ".join(videos) if videos else "не выбрано"),
            "Аудио: " + (Path(self.audio_file).name if self.audio_file and Path(self.audio_file).exists() else "не выбрано"),
            "Оверлей: " + (Path(self.overlay_file).name if self.overlay_file and Path(self.overlay_file).exists() else "не выбран"),
            "Результат: " + ("youtube_ready.mp4 готов" if (ROOT / "youtube_ready.mp4").exists() else "еще не создан"),
        ]
        self.status.setText("\n".join(lines))
        self.open_button.setEnabled((ROOT / "youtube_ready.mp4").exists())

    def reset_defaults(self):
        self.video_files = sorted((ROOT / "video").glob("source*.mp4"))
        self.audio_file = ROOT / "audio" / "voice.mp3"
        self.overlay_file = ROOT / "overlay.png"
        self.refresh_status()

    def choose_videos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите видеофайлы",
            str(ROOT),
            "Видео (*.mp4 *.mov *.mkv *.avi);;Все файлы (*.*)",
        )
        if files:
            self.video_files = [Path(file) for file in files]
            self.refresh_status()

    def choose_audio(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите аудиофайл",
            str(ROOT),
            "Аудио (*.mp3 *.wav *.m4a *.aac);;Все файлы (*.*)",
        )
        if file:
            self.audio_file = Path(file)
            self.refresh_status()

    def choose_overlay(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите PNG-оверлей",
            str(ROOT),
            "PNG (*.png);;Все файлы (*.*)",
        )
        if file:
            self.overlay_file = Path(file)
            self.refresh_status()

    def values(self):
        defaults = {
            "heading": "#ЗАГОЛОВОК",
            "name": "Имя",
            "extra": "Страна",
            "date": "Дата мероприятия",
        }
        values = {
            "heading": self.heading.text().strip() or defaults["heading"],
            "name": self.name.text().strip() or defaults["name"],
            "extra": self.extra.text().strip() or defaults["extra"],
            "date": self.date.text().strip() or defaults["date"],
        }
        for value in values.values():
            if len(value) > MAX_TEXT_LENGTH:
                raise ValueError("Каждое поле должно быть не длиннее 20 символов.")
        return values

    def append_log(self, text):
        self.log.moveCursor(self.log.textCursor().MoveOperation.End)
        self.log.insertPlainText(text)
        self.log.moveCursor(self.log.textCursor().MoveOperation.End)

    def prepare_inputs(self):
        if not self.video_files:
            raise ValueError("Выберите хотя бы один видеофайл.")
        missing_videos = [str(path) for path in self.video_files if not Path(path).exists()]
        if missing_videos:
            raise ValueError("Не найдены выбранные видеофайлы:\n" + "\n".join(missing_videos))
        if not self.audio_file or not Path(self.audio_file).exists():
            raise ValueError("Выберите один аудиофайл.")
        if not self.overlay_file or not Path(self.overlay_file).exists():
            raise ValueError("Выберите один PNG-оверлей.")

    def estimate_needed_space(self):
        selected_size = sum(Path(path).stat().st_size for path in self.video_files)
        selected_size += Path(self.audio_file).stat().st_size
        selected_size += Path(self.overlay_file).stat().st_size
        # The app creates a rendered intermediate file plus a looped silent video
        # before the final mp4. Keep this deliberately conservative.
        return max(selected_size * 4, 3 * 1024 * 1024 * 1024)

    def check_free_space(self):
        needed = self.estimate_needed_space()
        usage = shutil.disk_usage(ROOT)
        if usage.free < needed:
            free_gb = usage.free / (1024 ** 3)
            need_gb = needed / (1024 ** 3)
            raise ValueError(
                f"Недостаточно свободного места на диске.\n\n"
                f"Свободно: {free_gb:.1f} ГБ\n"
                f"Желательно иметь минимум: {need_gb:.1f} ГБ"
            )

    def start_build(self):
        try:
            values = self.values()
            self.prepare_inputs()
            self.check_free_space()
        except ValueError as error:
            QMessageBox.critical(self, "Replicator", str(error))
            return

        self.log.clear()
        self.append_log("Запуск сборки...\n")
        self.start_button.setEnabled(False)
        self.open_button.setEnabled(False)

        python_exe = ROOT / "python" / "python.exe"
        if not python_exe.exists():
            python_exe = Path(sys.executable)

        args = [
            str(ROOT / "replicator.py"),
            "--no-pause",
            "--heading",
            values["heading"],
            "--name",
            values["name"],
            "--extra",
            values["extra"],
            "--date",
            values["date"],
            "--audio",
            str(self.audio_file),
            "--overlay",
            str(self.overlay_file),
        ]
        for video in self.video_files:
            args.extend(["--video", str(video)])
        self.process = QProcess(self)
        env = self.process.processEnvironment()
        env.insert("PYTHONUTF8", "1")
        self.process.setProcessEnvironment(env)
        self.process.setWorkingDirectory(str(ROOT))
        self.process.readyReadStandardOutput.connect(self.read_process)
        self.process.readyReadStandardError.connect(self.read_process)
        self.process.finished.connect(self.finish_build)
        self.process.start(str(python_exe), args)

    def read_process(self):
        if not self.process:
            return
        data = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
        data += bytes(self.process.readAllStandardError()).decode("utf-8", errors="replace")
        if data:
            self.append_log(data)

    def finish_build(self, code, _status):
        self.start_button.setEnabled(True)
        self.refresh_status()
        if code == 0 and (ROOT / "youtube_ready.mp4").exists():
            self.append_log("\nГотово. Файл: youtube_ready.mp4\n")
        else:
            self.append_log(f"\nОшибка сборки. Код: {code}\n")
            QMessageBox.critical(self, "Replicator", "Сборка завершилась с ошибкой. Подробности в логе.")

    def open_result(self):
        result = ROOT / "youtube_ready.mp4"
        if not result.exists():
            QMessageBox.information(self, "Replicator", "Файл youtube_ready.mp4 еще не создан.")
            return
        try:
            if os.name == "nt":
                os.startfile(str(result))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(result)])
            else:
                subprocess.Popen(["xdg-open", str(result)])
        except Exception:
            try:
                subprocess.Popen(["explorer", "/select,", str(result)])
            except Exception:
                QMessageBox.information(self, "Replicator", f"Готовый файл находится здесь:\n{result}")


def main():
    os.chdir(ROOT)
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = ReplicatorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
