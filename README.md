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

## Features

- 🌐 **Text translation** using Gemini (via `google-genai` or `google-generativeai`)
- 🗂️ **File support**:
  - Plain text (`.txt`)
  - PDF (`.pdf`)
  - CSV (`.csv`)
  - Excel (`.xls`, `.xlsx`)
- 🔉 **Text-to-Speech (TTS)**:
  - Uses `gTTS` to generate MP3 audio files
  - In-app audio player
  - MP3 download option
- 📌 **User-friendly interface** built with Streamlit:
  - Tabs for "Type Text" and "Upload File"
  - Language dropdown
  - Clear error messages and status indicators

---

## Architecture Overview

The application follows a simple layered architecture:

1. **UI Layer (Streamlit)**
   - Handles user interactions (text input, file upload, language selection, button clicks).
   - Displays original text, translated text, and audio playback.

2. **Service Layer**
   - `GeminiClient`  
     - Wraps the Gemini API client and sends translation prompts.
   - `TranslationService`  
     - Uses `GeminiClient` to translate input text.
   - `TextToSpeechService`  
     - Uses `gTTS` to generate MP3 audio files from translated text.

3. **Utility Layer**
   - `FileProcessor`  
     - Reads uploaded files (TXT, PDF, CSV, Excel).
     - Extracts and normalizes text from each file type.

4. **Configuration**
   - `config/languages.py` maintains a mapping between user-facing language names and language codes used by gTTS.

A more detailed description is available in `docs/architecture.md`.

5. **Repository Structure**
## Repository Structure

```text
.
├── app.py                   # Streamlit entrypoint
├── requirements.txt
├── .gitignore
├── README.md
├── docs/
│   └── architecture.md        # High-level design / architecture document
|   └── technical_flow.md      # High-level technical flow document 
├── config/
│   └── languages.py         # Language mappings (name -> code)
├── services/
│   ├── gemini_client.py     # Low-level Gemini API wrapper
│   ├── translator.py        # TranslationService using GeminiClient
│   └── tts_service.py       # TextToSpeechService using gTTS
├── utils/
│   └── file_processor.py    # Extract text from TXT/PDF/CSV/Excel uploads
└── tests/
    ├── test_translator.py
    ├── test_file_processor.py
    └── test_tts_service.py
```

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