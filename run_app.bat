@echo off
echo Starting MediChain AI Application...
echo.

REM Try to find Python
set PYTHON_PATH=

REM Check common Python locations
if exist "C:\Program Files\Python312\python.exe" (
    set PYTHON_PATH="C:\Program Files\Python312\python.exe"
    goto :found_python
)

if exist "C:\Program Files (x86)\Python312\python.exe" (
    set PYTHON_PATH="C:\Program Files (x86)\Python312\python.exe"
    goto :found_python
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON_PATH="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    goto :found_python
)

if exist "C:\Python312\python.exe" (
    set PYTHON_PATH="C:\Python312\python.exe"
    goto :found_python
)

REM Try to use python from PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_PATH=python
    goto :found_python
)

echo Python not found! Please install Python 3.12
echo You can download it from: https://www.python.org/downloads/
pause
exit /b 1

:found_python
echo Found Python at: %PYTHON_PATH%
echo.

REM Install dependencies
echo Installing required packages...
%PYTHON_PATH% -m pip install flask cryptography numpy pandas lxml xmltodict requests
echo.

REM Run the application
echo Starting MediChain AI...
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
%PYTHON_PATH% app.py

pause



