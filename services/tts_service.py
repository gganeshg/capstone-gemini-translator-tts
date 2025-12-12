import tempfile
from gtts import gTTS

class TextToSpeechService:
    def synthesize(self, text: str, lang_code: str) -> str:
        if not text.strip():
            raise ValueError("Cannot synthesize empty text.")

        tts = gTTS(text=text, lang=lang_code)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        return tmp_file.name