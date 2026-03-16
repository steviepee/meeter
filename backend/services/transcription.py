# Whisper — Phase 5
import io
from faster_whisper import WhisperModel

_model = WhisperModel("base", device="cpu", compute_type="int8")


def transcribe_chunk(audio_bytes: bytes) -> str:
    audio_file = io.BytesIO(audio_bytes)
    segments, _ = _model.transcribe(audio_file)
    return " ".join(seg.text.strip() for seg in segments)
