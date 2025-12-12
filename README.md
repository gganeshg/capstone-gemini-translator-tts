# capstone-gemini-translator-tts
Captstone Project for Tranlator(Gemini API and GTTS)

---

```markdown

## 1. Introduction

This document describes the architecture and design of the **Text Translator & Text-to-Speech Web App** built using Streamlit, Gemini, and gTTS. The goal of the system is to provide an easy-to-use interface for translating user-provided content into multiple languages and generating speech audio from the translated text.

## 2. Functional Requirements

- Accept user input as:
  - Free-form text
  - Uploaded file (TXT, PDF, CSV, Excel)
- Allow the user to select a target language.
- Translate the input text to the selected language using Gemini.
- Convert the translated text to speech and return an MP3 audio file.
- Provide an in-browser audio player and a download option for the audio.

## 3. Non-Functional Requirements

- Simple and intuitive UI (Streamlit).
- Clear error handling and user feedback.
- Secure handling of API keys (no keys in source code).
- Reasonable performance for typical text sizes (e.g., up to a few pages of text).

## 4. High-Level Architecture

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

## 5. Component Design

### 5.1 GeminiClient

- **Responsibilities:**
  - Initialize the Gemini client using an API key from environment variables.
  - Build translation prompts.
  - Send requests to the Gemini model.
  - Return the translated text.

- **Key Method:**
  - `translate(text: str, target_language: str) -> str`

### 5.2 TranslationService

- **Responsibilities:**
  - Validate input.
  - Call `GeminiClient` to perform translation.
  - Provide a simple interface to the UI for translation.

- **Key Method:**
  - `translate_text(text: str, target_language_name: str) -> str`

### 5.3 TextToSpeechService

- **Responsibilities:**
  - Accept translated text and a language code.
  - Use `gTTS` to generate speech audio.
  - Save the output as an MP3 file on disk and return the file path.

- **Key Method:**
  - `synthesize(text: str, lang_code: str) -> str`

### 5.4 FileProcessor

- **Responsibilities:**
  - Inspect the uploaded file type.
  - For TXT: read and decode text.
  - For PDF: use `PyPDF2` to extract text from each page.
  - For CSV/Excel: use `pandas` to read tabular data and join cell contents into lines of text.

- **Key Method:**
  - `extract_text(file) -> str`

## 6. Data Flow

1. User opens the Streamlit app and selects a target language.
2. User either types text or uploads a file.
3. If a file is uploaded, `FileProcessor.extract_text()` converts it into plain text.
4. When the user clicks **Translate**, the app calls `TranslationService.translate_text()`.
5. `TranslationService` uses `GeminiClient.translate()` to get the translated text.
6. The translated text is displayed to the user.
7. When the user clicks **Generate Audio**, the app calls `TextToSpeechService.synthesize()`.
8. The resulting MP3 file is loaded into the Streamlit app and can be played or downloaded.

## 7. Error Handling

- Empty input text → validation error message in UI.
- Unsupported file type → error message from `FileProcessor`.
- Missing or invalid `GEMINI_API_KEY` → handled in `GeminiClient` with a clear error.
- External service errors (Gemini, gTTS) → caught and displayed in the UI via `st.error()`.

## 8. Testing Strategy

- **Unit Tests:**
  - Test translation logic with a dummy or mocked `GeminiClient`.
  - Test file extraction for different file types using small sample files.
  - Test text-to-speech to ensure an MP3 file is created for non-empty input.

- **Manual Tests:**
  - Translate various text snippets in different languages.
  - Upload PDF/TXT/CSV/Excel files and verify extracted and translated content.
  - Verify that audio playback and download work in the browser.

## 9. Future Enhancements

- Add support for more languages and voices.
- Implement user account and history of translations.
- Allow users to adjust speaking rate and pitch.
- Support longer documents with streaming or chunking.
