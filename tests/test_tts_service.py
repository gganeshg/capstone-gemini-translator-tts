# tests/test_tts_service.py
import os
from services.tts_service import TextToSpeechService

def test_tts_empty():
    tts = TextToSpeechService()
    try:
        tts.synthesize("", "en")
        assert False, "Expected ValueError"
    except ValueError:
        assert True

def test_tts_creates_file():
    tts = TextToSpeechService()
    path = tts.synthesize("Hello world", "en")
    assert os.path.exists(path)
    assert path.endswith(".mp3")
