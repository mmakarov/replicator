@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
set QT_OPENGL=software

if exist "python\pythonw.exe" (
  start "" "python\pythonw.exe" "gui_qt.py"
) else if exist "python\python.exe" (
  "python\python.exe" "gui_qt.py"
) else (
  py -3 "gui_qt.py"
)

if errorlevel 1 (
  echo.
  echo Приложение завершилось с ошибкой.
  pause
)
