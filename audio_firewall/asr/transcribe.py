from faster_whisper import WhisperModel

def transcribe_audio(audio_path, model_size="base"):
    model = WhisperModel(model_size, compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    transcript = []
    for seg in segments:
        transcript.append({
            "start": float(seg.start),
            "end": float(seg.end),
            "text": seg.text.strip()
        })
    return transcript
