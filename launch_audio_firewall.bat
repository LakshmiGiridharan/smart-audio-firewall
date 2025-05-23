@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

cd /d %~dp0

echo Activating virtual environment...
call venv\\Scripts\\activate.bat

echo Launching Smart Audio Firewall...
streamlit run audio_firewall/frontend.py --server.port 8501
IF ERRORLEVEL 1 (
    echo Port 8501 in use. Trying backup port 8502...
    streamlit run audio_firewall/frontend.py --server.port 8502
)
