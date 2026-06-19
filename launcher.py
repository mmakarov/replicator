#!/usr/bin/env python
import ctypes
import os
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "startup.log"


def smoke_test():
    os.environ.setdefault("QT_OPENGL", "software")
    import gui_qt
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(["replicator-smoke"])
    window = gui_qt.ReplicatorWindow()
    app.processEvents()
    if not window.windowTitle():
        raise RuntimeError("Replicator window was not initialized")
    print("Replicator GUI smoke OK")
    window.close()
    window.deleteLater()
    app.processEvents()
    app.quit()


def show_error(message):
    if os.environ.get("REPLICATOR_SMOKE") == "1" or "--smoke" in sys.argv:
        print(message)
        return
    try:
        ctypes.windll.user32.MessageBoxW(None, message, "Replicator", 0x10)
    except Exception:
        print(message)


def main():
    os.chdir(ROOT)
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("QT_OPENGL", "software")
    try:
        if "--smoke" in sys.argv or os.environ.get("REPLICATOR_SMOKE") == "1":
            smoke_test()
            return

        import gui_qt

        gui_qt.main()
    except Exception:
        details = traceback.format_exc()
        LOG_FILE.write_text(details, encoding="utf-8", errors="replace")
        show_error(
            "Приложение не смогло запуститься.\n\n"
            "Рядом с запускателем создан файл startup.log.\n"
            "Отправьте его разработчику."
        )
        raise


if __name__ == "__main__":
    main()
