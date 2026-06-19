@echo off
chcp 65001 >nul
setlocal
pushd "%~dp0"
set PYTHONUTF8=1
set QT_OPENGL=software
set PATH=%CD%\python;%CD%\python\Lib\site-packages\PySide6;%PATH%
set QT_PLUGIN_PATH=%CD%\python\Lib\site-packages\PySide6\plugins

if not exist "python\python.exe" goto no_python
if not exist "launcher.py" goto no_launcher

"python\python.exe" "launcher.py"
set APP_ERROR=%ERRORLEVEL%
if not "%APP_ERROR%"=="0" goto app_error

popd
exit /b 0

:no_python
echo.
echo   Ñ python\python.exe.
echo , ÄÖ Ä  Çåé.
pause
popd
exit /b 1

:no_launcher
echo.
echo   Ñ launcher.py.
echo , ÄÖ Ä  Çåé.
pause
popd
exit /b 1

:app_error
echo.
echo Ä Äàå  à.
echo  Ä  startup.log  render.log, ÇÄåÇ çÇÇ Ñ ÄÄÇáÉ.
pause
popd
exit /b %APP_ERROR%
