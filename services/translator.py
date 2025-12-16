from .gemini_client import GeminiClient

class TranslationService:
    def __init__(self, gemini_client=None):
        self.client = gemini_client or GeminiClient()

    def translate_text(self, text: str, target_language_name: str) -> str:
        if not text and not text.strip():
            raise ValueError("Input text is empty.")

        lines = text.splitlines()

        translated_lines = []
        for line in lines:
            if not line and not line.strip():
                translated_lines.append(line)
                continue
            translated_lines.append(self.client.translate(line, target_language_name))

        return "\n".join(translated_lines)