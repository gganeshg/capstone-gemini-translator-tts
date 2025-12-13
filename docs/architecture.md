## High-Level Architecture

The system is organized into three main layers:

1. **Presentation Layer (Streamlit UI)**  
   - Provides the web interface.
   - Handles user input (text, files, language choice).
   - Triggers translation and audio generation actions.
   - Displays results and error messages.

2. **Application / Service Layer**
   - `GeminiClient`: Low-level wrapper around the Gemini API.
   - `TranslationService`: Business logic for translating text.
   - `TextToSpeechService`: Business logic for converting text to speech using gTTS.

3. **Utility Layer**
   - `FileProcessor`: Responsible for reading uploaded files and extracting plain text.

Configuration, such as supported languages, is stored in `config/languages.py`.

## Component Design

### 1. GeminiClient

- **Responsibilities:**
  - Initialize the Gemini client using an API key from environment variables.
  - Build translation prompts.
  - Send requests to the Gemini model.
  - Return the translated text.

- **Key Method:**
  - `translate(text: str, target_language: str) -> str`

### 2 TranslationService

- **Responsibilities:**
  - Validate input.
  - Call `GeminiClient` to perform translation.
  - Provide a simple interface to the UI for translation.

- **Key Method:**
  - `translate_text(text: str, target_language_name: str) -> str`

### 3 TextToSpeechService

- **Responsibilities:**
  - Accept translated text and a language code.
  - Use `gTTS` to generate speech audio.
  - Save the output as an MP3 file on disk and return the file path.

- **Key Method:**
  - `synthesize(text: str, lang_code: str) -> str`

### 4 FileProcessor

- **Responsibilities:**
  - Inspect the uploaded file type.
  - For TXT: read and decode text.
  - For PDF: use `PyPDF2` to extract text from each page.
  - For CSV/Excel: use `pandas` to read tabular data and join cell contents into lines of text.

- **Key Method:**
  - `extract_text(file) -> str`

# Text Translator & Text-to-Speech Web App (Gemini + gTTS + Streamlit)

This project is a web-based application that translates text into multiple languages using Google's Gemini API and then converts the translated text into speech using gTTS (Google Text-to-Speech). The user interacts with the app through a simple Streamlit interface.

The app supports:
- Direct text input
- File uploads (TXT / PDF / CSV / Excel)
- Translation to multiple languages
- Audio generation (MP3) for the translated text

---