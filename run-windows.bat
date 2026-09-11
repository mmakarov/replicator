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
echo python\python.exe was not found.
echo The archive may not have been extracted completely.
if "%REPLICATOR_SMOKE%"=="1" goto no_python_exit
pause
:no_python_exit
popd
exit /b 1

:no_launcher
echo.
echo launcher.py was not found.
echo The archive may not have been extracted completely.
if "%REPLICATOR_SMOKE%"=="1" goto no_launcher_exit
pause
:no_launcher_exit
popd
exit /b 1

:app_error
echo.
echo The application exited with an error.
echo If startup.log or render.log appeared next to the app, send that file to the developer.
if "%REPLICATOR_SMOKE%"=="1" goto app_error_exit
pause
:app_error_exit
popd
exit /b %APP_ERROR%
