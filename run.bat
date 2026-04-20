@echo off
echo Starting MediChain Server...
echo.
cd /d "%~dp0"
.venv\Scripts\python.exe app.py
pause
