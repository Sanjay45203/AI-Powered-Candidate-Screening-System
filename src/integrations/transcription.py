import os

def transcribe_audio(audio_path: str) -> dict:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Install faster-whisper to enable transcription.") from exc
    model = WhisperModel(
        os.getenv("WHISPER_MODEL", "small"),
        device=os.getenv("WHISPER_DEVICE", "cpu"),
        compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8")
    )
    segments, info = model.transcribe(audio_path, vad_filter=True)
    parts = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segments]
    return {"language": info.language, "text": " ".join(p["text"] for p in parts), "segments": parts}
