import os
from google import genai

class GeminiClient:
    def __init__(self, api_key: str | None = None, model: str = "gemini-2.5-flash"):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set.")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def translate(self, text: str, target_language: str) -> str:
        """
        Use Gemini as a translation engine via prompt.
        target_language: e.g. 'Spanish', 'French' (natural language).
        """
        prompt = (
            f"Translate the following text into {target_language}. "
            f"Return only the translated text without explanations.\n\n{text}"
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return (response.text or "").strip()
