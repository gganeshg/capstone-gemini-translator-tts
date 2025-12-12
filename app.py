import streamlit as st

from config.languages import LANGUAGE_OPTIONS
from services.translator import TranslationService
from services.tts_service import TextToSpeechService
from utils.file_processor import FileProcessor

st.set_page_config(page_title="Gemini Translator + TTS", layout="wide")

translator = TranslationService()
tts_service = TextToSpeechService()
file_processor = FileProcessor()

st.title("🌐 Text Translator & Text-to-Speech (Gemini + gTTS)")

st.sidebar.header("Settings")
target_language_name = st.sidebar.selectbox(
    "Choose target language",
    list(LANGUAGE_OPTIONS.keys()),
    index=1,  # default maybe Spanish
)
target_lang_code = LANGUAGE_OPTIONS[target_language_name]

st.sidebar.markdown(
    """
    **How to use:**
    1. Type text or upload a file (PDF/TXT/CSV/Excel).
    2. Click **Translate** to see translated text.
    3. Click **Generate Audio** to get mp3 and listen/download.
    """
)

tab1, tab2 = st.tabs(["✍️ Type Text", "📁 Upload File"])

input_text = ""

with tab1:
    st.subheader("Enter text to translate")
    input_text = st.text_area("Enter text here", height=200, key="text_input")

with tab2:
    st.subheader("Upload a file")
    uploaded_file = st.file_uploader(
        "Upload PDF, TXT, CSV, or Excel",
        type=["pdf", "txt", "csv", "xls", "xlsx"],
        key="file_upload"
    )
    if uploaded_file is not None and not input_text.strip():
        try:
            input_text = file_processor.extract_text(uploaded_file)
            st.success("File loaded successfully. You can review the extracted text below.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

if input_text:
    st.markdown("**Extracted / Original Text:**")
    st.text_area("Source text", value=input_text, height=200, key="source_text_display")

translated_text = st.session_state.get("translated_text", "")

col1, col2 = st.columns(2)

with col1:
    if st.button("Translate"):
        if not input_text.strip():
            st.error("Please provide text or upload a file.")
        else:
            with st.spinner("Translating..."):
                try:
                    translated_text = translator.translate_text(
                        input_text, target_language_name
                    )
                    st.session_state["translated_text"] = translated_text
                    st.success("Translation completed!")
                except Exception as e:
                    st.error(f"Translation failed: {e}")

with col2:
    audio_file_path = None
    if st.button("Generate Audio"):
        translated_text = st.session_state.get("translated_text", "")
        if not translated_text:
            st.error("Please translate the text first.")
        else:
            with st.spinner("Generating audio..."):
                try:
                    audio_file_path = tts_service.synthesize(
                        translated_text, target_lang_code
                    )
                    st.session_state["audio_file_path"] = audio_file_path
                    st.success("Audio generated!")
                except Exception as e:
                    st.error(f"Text-to-Speech failed: {e}")

# Display translation
translated_text = st.session_state.get("translated_text", "")
if translated_text:
    st.markdown("### Translated Text")
    st.text_area("Translated output", translated_text, height=200)
# Display audio
audio_file_path = st.session_state.get("audio_file_path")
if audio_file_path:
    st.markdown("### 🎧 Listen / Download Audio")
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
        st.download_button(
            label="Download MP3",
            data=audio_bytes,
            file_name="translated_audio.mp3",
            mime="audio/mp3",
        )