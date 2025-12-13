 ┌──────────────────────────┐
 │        Streamlit UI      │
 │──────────────────────────│
 │ • Text Input             │
 │ • File Upload            │
 │ • Language Selection     │
 │ • Display Text & Audio   │
 └─────────────┬────────────┘
               │
               ▼
 ┌───────────────────────────────────────────────-┐
 │               Service Layer                    │
 │───────────────────────────────────────────────-│
 │                                                │
 │   ┌────────────────┐   ┌──────────────────┐    │
 │   │ GeminiClient   │   │ TranslatorService│    │
 │   │ (API Wrapper)  │   │ (Calls Gemini)   │    │
 │   └────────────────┘   └──────────────────┘    │
 │                     ┌──────────────────────┐   │
 │                     │ TextToSpeechService  │   │
 │                     │  (gTTS Audio Output) │   │
 │                     └──────────────────────┘   │
 └─────────────┬──────────────────────────────────┘
               │
               ▼
 ┌───────────────────────────────────────────────┐
 │                 Utility Layer                 │
 │───────────────────────────────────────────────│
 │                                               │
 │   • FileProcessor                             │
 │     - Reads TXT / PDF / CSV / Excel           │
 │     - Extracts & cleans text                  │
 └───────────────────────────────────────────────┘

                  ▲
                  │
      ┌────────────────────────────┐
      │     Configuration Layer    │
      │────────────────────────────│
      │  config/languages.py       │
      │  • Language name → code    │
      │  • Used by UI dropdown     │
      │  • Used by TTS service     │
      └────────────────────────────┘
