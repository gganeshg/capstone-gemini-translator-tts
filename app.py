import streamlit as st

from config.languages import LANGUAGE_OPTIONS
from services.translator import TranslationService
from services.tts_service import TextToSpeechService
from utils.file_processor import FileProcessor

st.set_page_config(page_title="Gemini Translator + TTS", layout="wide")

translator = TranslationService()
tts_service = TextToSpeechService()
file_processor = FileProcessor()

# ---- Initialize session state keys ----
if "source_text_display" not in st.session_state:
    st.session_state["source_text_display"] = ""
if "translated_text" not in st.session_state:
    st.session_state["translated_text"] = ""
if "audio_file_path" not in st.session_state:
    st.session_state["audio_file_path"] = None

st.title("🌐 Text Translator & Text-to-Speech (Gemini + gTTS)")

st.sidebar.header("Settings")
target_language_name = st.sidebar.selectbox(
    "Choose target target language",
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

# We keep manual text and uploaded text separate, and use source_text_display
# as the single "authoritative" text to translate.

with tab1:
    st.subheader("Enter text to translate")
    # Streamlit will store this in st.session_state["text_input"]
    st.text_area("Enter text here", height=200, key="text_input")

with tab2:
    st.subheader("Upload a file")
    uploaded_file = st.file_uploader(
        "Upload PDF, TXT, CSV, or Excel",
        type=["pdf", "txt", "csv", "xls", "xlsx"],
        key="file_upload"
    )
    if uploaded_file is not None:
        try:
            extracted_text = file_processor.extract_text(uploaded_file) or ""
            extracted_text = extracted_text.strip()
            # st.write("DEBUG type:", type(extracted_text), "len:", len(extracted_text))

            if not extracted_text:
                st.error("Uploaded file appears to be empty or could not be read. Please try again.")
            else:
                st.session_state["source_text_display"] = extracted_text
                st.success("File loaded successfully.")    
                # Always replace the source text with the new file content 
                # st.session_state["source_text_display"] = extracted_text
                # st.success("File loaded successfully. You can review the extracted text below.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# ---- Decide what the current source text is ----
current_source_text = st.session_state.get("source_text_display", "")
manual_text = st.session_state.get("text_input", "")

# If there is no uploaded/edited source text yet, but the user has typed something,
# initialize source_text_display from the manual text.
if not current_source_text and manual_text.strip():
    st.session_state["source_text_display"] = manual_text
    current_source_text = manual_text

# Show the combined "Extracted / Original Text" area if we have any text at all
if current_source_text.strip():
    st.markdown("**Extracted / Original Text:**")
    # This text_area is bound directly to source_text_display; any edits here
    # become the text that will be translated.
    st.text_area(
        "Source text",
        height=200,
        key="source_text_display"
    )

# For translation logic, always use whatever is currently in source_text_display
input_text = st.session_state.get("source_text_display", "")

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
    # Debug Statements
    # st.write("Lines extracted:", len(input_text.splitlines()))
    # st.text_area("Debug: extracted preview", input_text[:2000], height=200)
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
