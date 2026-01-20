@echo off
echo Starting Launcher... > bat_debug.log
py -3.11 debug_web_launcher.py >> bat_debug.log 2>&1
if %errorlevel% neq 0 (
    echo CRASHED with code %errorlevel% >> bat_debug.log
) else (
    echo FINISHED >> bat_debug.log
)
