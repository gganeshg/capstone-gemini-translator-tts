from .gemini_client import GeminiClient

class TranslationService:
    def __init__(self, gemini_client: GeminiClient | None = None):
        self.client = gemini_client or GeminiClient()

    def translate_text(self, text: str, target_language_name: str) -> str:
        if not text.strip():
            raise ValueError("Input text is empty.")
        return self.client.translate(text, target_language_name)