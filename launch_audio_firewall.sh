#!/bin/bash

cd "$(dirname "$0")"

echo " Killing old Streamlit processes..."
pkill -f "streamlit run"

# Activate or create venv
if [ -d "venv" ]; then
    echo " Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️ venv not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install Python dependencies
echo " Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo " ffmpeg is not installed."
    echo "To install it, run the appropriate command:"
    echo " macOS: brew install ffmpeg"
    echo " Ubuntu: sudo apt install ffmpeg"
    echo " Windows: https://ffmpeg.org/download.html"
    exit 1
fi

# Try ports 8501–8510
for port in {8501..8510}; do
    echo " Trying port $port..."
    streamlit run audio_firewall/frontend.py --server.port $port && break
    echo "Port $port in use. Trying next..."
done
