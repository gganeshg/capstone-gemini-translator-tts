# tests/test_translator.py
import pytest
from services.translator import TranslationService

class DummyGeminiClient:
    def translate(self, text, target_language):
        return f"[{target_language}] {text}"
        

def test_translate_text_success():
    service = TranslationService(gemini_client=DummyGeminiClient())
    result = service.translate_text("Hello", "Spanish")
    assert result == "[Spanish] Hello"

def test_translate_text_empty():
    service = TranslationService(gemini_client=DummyGeminiClient())
    with pytest.raises(ValueError):
        service.translate_text("   ", "Spanish")