#  Smart Audio Firewall

A Streamlit app that analyzes or records audio to detect sensitive content.

## How to Run

1. **Clone the repo and enter the folder**  
   ```bash
      cd audio_firewall
   ```

2. **(Optional) Install Homebrew** (macOS only)  
   If you don’t have Homebrew installed:  
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install `ffmpeg`**  
   ```bash
   brew install ffmpeg
   ```

4. **Give execution permission to the script**  
   ```bash
   chmod +x launch_audio_firewall.sh
   ```

5. **Launch the app**  
   ```bash
   ./launch_audio_firewall.sh
   ```

6. **Usage**  
   - Enter a report filename when prompted  
   - Upload or record audio input  
   - View flagged segments and download the report.