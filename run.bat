@echo off
cd /d "%~dp0"
title MovieSphere - FastAPI Server
if not exist .venv (
    echo Creating virtual environment...
    py -m venv .venv
    if errorlevel 1 python -m venv .venv
)
call .venv\Scripts\activate
if errorlevel 1 (
    echo Could not activate the virtual environment.
    pause
    exit /b 1
)
echo Installing required packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed. Check the error above.
    pause
    exit /b 1
)
echo.
echo Starting MovieSphere...
echo Keep this window open while using the website.
echo Open http://127.0.0.1:8000 in your browser.
echo.
python -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
