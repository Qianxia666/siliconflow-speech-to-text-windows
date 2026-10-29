@echo off
setlocal
cd /d "%~dp0"

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
  echo Python was not found. Install Python 3.9+ and enable "Add python.exe to PATH".
  pause
  exit /b 1
)

echo [2/3] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
  echo Failed to install dependencies.
  pause
  exit /b 1
)

echo [3/3] Building SiliconflowSTT.exe...
python -m PyInstaller --noconfirm --clean --onefile --console --name SiliconflowSTT --add-data "templates;templates" --add-data "static;static" app.py
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)

echo.
echo Done: dist\SiliconflowSTT.exe
echo Put a .env file next to the exe before running it.
pause
