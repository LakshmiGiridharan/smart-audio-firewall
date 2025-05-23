import json
from asr.transcribe import transcribe_audio
from nlp.flag_sensitive import load_keywords, flag_transcript
from utils.redact import redact_text

AUDIO_PATH = "data/example.wav"
USER_KEYWORDS = [
    "salary", "fired", "religion", "mental health", "Project X", "nda", "divorce"
]

def main():
    print("[*] Transcribing...")
    transcript = transcribe_audio(AUDIO_PATH)

    print("[*] Embedding keywords...")
    keyword_embeddings = load_keywords(USER_KEYWORDS)

    print("[*] Flagging sensitive segments...")
    flagged = flag_transcript(transcript, keyword_embeddings, USER_KEYWORDS)

    print("[*] Redacting transcript...")
    full_text = " ".join([seg['text'] for seg in transcript])
    redacted = redact_text(full_text, USER_KEYWORDS)

    output = {
        "transcript": transcript,
        "flags": flagged,
        "redacted_transcript": redacted
    }

    with open("output/flagged_output.json", "w") as f:
        json.dump(output, f, indent=2)

    print("[✓] Done. Output saved to output/flagged_output.json")

if __name__ == "__main__":
    main()
