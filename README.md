#  Smart Audio Firewall

A Streamlit app that analyzes or records audio to detect sensitive content.

**System Architechture**
                   ┌──────────────────────────────┐
                   │        User Interface        │
                   │  (Streamlit Web Frontend)    │
                   └────────────┬─────────────────┘
                                │
                    User uploads audio / records via mic
                                │
                                ▼
           ┌──────────────────────────────────────────┐
           │           Audio Processing Module         │
           │  - Converts input to .wav (via Pydub)      │
           │  - Saves file locally for analysis         │
           └────────────────────────────┬──────────────┘
                                        │
                                        ▼
                  ┌─────────────────────────────────┐
                  │      Speech-to-Text Engine       │
                  │      (Faster-Whisper / Whisper)  │
                  └────────────────────┬─────────────┘
                                       │ Transcription
                                       ▼
                  ┌──────────────────────────────────┐
                  │  NLP & Semantic Flagging Module  │
                  │  - Loads predefined sensitive     │
                  │    keywords (1000+)               │
                  │  - Computes cosine similarity     │
                  │    via Sentence Transformers      │
                  │  - Classifies severity (warning/  │
                  │    critical)                      │
                  └────────────────────┬──────────────┘
                                       │
                                       ▼
                ┌───────────────────────────────────────┐
                │   Explainability & Redaction Engine   │
                │   - Redacts flagged terms             │
                │   - Summarizes risky topics           │
                │   - Adds timestamps and context       │
                └────────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌────────────────────────────────┐
                  │     Report Generation Module    │
                  │  - Full transcript              │
                  │  - Redacted version             │
                  │  - Flagged segments with scores │
                  │  - Summary of issues            │
                  └────────────────────────────────┘

**System Flow**
launch_audio_firewall.sh: Bootstraps environment and launches Streamlit app

frontend.py: Handles UI, session state, and pipeline orchestration

asr/transcribe.py: Transcribes audio using Whisper

nlp/flag_sensitive.py: Embedding-based keyword detection

nlp/summarize.py: Generates natural language summary (optional)

utils/redact.py: Redacts sensitive keywords from transcript

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
   (if windows then use) ./launch_audio_firewall.bat
   ```

6. **Usage**  
   - Enter a report filename when prompted  
   - Upload or record audio input  
   - View flagged segments and download the report.
