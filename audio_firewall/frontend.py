# Smart Audio Firewall - Streamlit Frontend
# Built by a developer with 3+ months experience to ensure smooth, modular UX

import streamlit as st
import tempfile
import os
import sounddevice as sd
import scipy.io.wavfile as wav
from pydub import AudioSegment
from asr.transcribe import transcribe_audio
from nlp.flag_sensitive import load_keywords, flag_transcript
from utils.redact import redact_text
from nlp.summarize import summarize_flags

# Helper function to record mic input
def record_audio(duration=5, sample_rate=44100):
    st.info(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        wav.write(temp_file.name, sample_rate, audio)
        return temp_file.name

# ------------------- UI Layout Begins -------------------
st.set_page_config(page_title="Smart Audio Firewall", layout="centered")
st.title(" Smart Audio Firewall")

# Step 1: Ask user to enter a file name first
if "filename_entered" not in st.session_state:
    st.session_state.filename_entered = False

if not st.session_state.filename_entered:
    filename_input = st.text_input(" Name your report file (no extension needed):", value="audio_report")
    if st.button(" Confirm File Name"):
        if filename_input.strip():
            cleaned_name = filename_input.strip()
            if not cleaned_name.endswith(".txt"):
                cleaned_name += ".txt"
            st.session_state.file_name = cleaned_name
            st.session_state.filename_entered = True
        else:
            st.warning("Please enter a valid file name to proceed.")
    st.stop()

# Step 2: Let user provide audio - upload or record
input_choice = st.radio("Choose how you'd like to provide audio:", ("Upload Audio File", "Record via Microphone"))

if input_choice == "Upload Audio File":
    uploaded = st.file_uploader("Upload .wav, .mp3, or .m4a audio", type=["wav", "mp3", "m4a"])
    if uploaded:
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        AudioSegment.from_file(uploaded).export(temp_path, format="wav")
        st.session_state.audio_path = temp_path
        st.audio(uploaded)

elif input_choice == "Record via Microphone":
    dur = st.slider(" Set recording duration (seconds):", 3, 15, 5)
    if st.button(" Start Recording"):
        recorded_path = record_audio(duration=dur)
        st.session_state.audio_path = recorded_path
        st.audio(recorded_path)

# Step 3: Process the audio using Whisper + LLM pipeline
if "audio_path" in st.session_state:
    if st.button(" Run Analysis"):
        st.success("Audio processed. Click below to view insights.")

        transcript_data = transcribe_audio(st.session_state.audio_path)
        full_text = " ".join([seg['text'] for seg in transcript_data])

        sensitive_keywords = [
    "salary", "pay", "bonus", "raise", "compensation", "income", "wages", "hourly rate", "overtime", "CTC",
    "fired", "laid off", "terminated", "dismissed", "let go", "job loss", "downsizing", "unemployed", "offboarded", "pink slip",
    "mental health", "depression", "anxiety", "therapy", "counseling", "stress", "burnout", "PTSD", "bipolar", "psychologist",
    "nda", "non-disclosure", "leak", "violation", "confidentiality", "signed agreement", "internal doc", "compliance breach", "legal hold", "contract",
    "confidential", "private", "classified", "hidden", "restricted", "internal use", "redacted", "undisclosed", "privileged", "eyes only",
    "project x", "secret project", "unannounced", "code-named", "prototype", "pilot", "stealth", "internal test", "early access", "initiative",
    "termination", "contract end", "exit interview", "disciplinary", "retirement", "early exit", "voluntary leave", "resignation", "HR action", "final notice",
    "divorce", "separation", "custody", "alimony", "marriage problems", "breakup", "ex-spouse", "court filing", "legal separation", "family dispute"
]


        keyword_embeddings = load_keywords(sensitive_keywords)
        flagged = flag_transcript(transcript_data, keyword_embeddings, sensitive_keywords, threshold=0.2)
        redacted_version = redact_text(full_text, sensitive_keywords)
        summary_text = summarize_flags(flagged, user_keywords=sensitive_keywords) if flagged else "No flagged segments found."

        # Save all to session
        st.session_state.transcript = transcript_data
        st.session_state.full_text = full_text
        st.session_state.flags = flagged
        st.session_state.redacted = redacted_version
        st.session_state.summary = summary_text

# Step 4: Show results and allow export
if "flags" in st.session_state and st.button(" Show Output", key="show_output_button"):
    st.subheader(" Full Transcript")
    st.text(st.session_state.full_text)

    st.subheader(" Flagged Segments")
    for flag in st.session_state.flags:
        st.markdown(f"** {flag['timestamp']}** — *{flag['flag'].upper()}*")
        st.text(flag['text'])
        st.progress(min(flag['score'], 1.0))

    st.subheader("Redacted Transcript")
    st.text(st.session_state.redacted)

    st.subheader("📘 Transcript with Timestamps")
    for seg in st.session_state.transcript:
        st.markdown(f"** {seg['start']:.2f}–{seg['end']:.2f}**")
        st.text(seg['text'])

    st.subheader("Summary of Red Flags")
    st.success(st.session_state.summary)

    # Generate readable report text
    lines = [
        " SMART AUDIO FIREWALL REPORT\n",
        "=== Summary of Red Flags ===",
        st.session_state.get("summary", "No summary available."),
        "\n\n=== Redacted Transcript ===",
        st.session_state.get("redacted", "N/A"),
        "\n\n=== Flagged Segments ==="
    ]

    for f in st.session_state.get("flags", []):
        lines.append(f" {f['timestamp']} — [{f['flag'].upper()}] {f['text']}")

    lines.append("\n\n=== Full Transcript ===")
    for seg in st.session_state.get("transcript", []):
        lines.append(f"{seg['start']:.2f}–{seg['end']:.2f}: {seg['text']}")

    readable_output = "\n".join(lines)

    st.download_button(
        label="Download Report",
        data=readable_output,
        file_name=st.session_state.get("file_name", "smart_audio_firewall_report.txt"),
        mime="text/plain"
    )