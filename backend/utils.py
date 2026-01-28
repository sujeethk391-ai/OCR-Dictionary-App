# utils.py
from googletrans import Translator
from gtts import gTTS
import base64
import io

# Initialize the translator once
translator = Translator()

def translate_text(text: str) -> str:
    """Translates French text to English."""
    try:
        # Source language: French (fr), Destination language: English (en)
        translation = translator.translate(text, src='fr', dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation Error: {e}")
        return "Error: Could not translate text."

def get_pronunciation_audio(text: str) -> str:
    """
    Generates an MP3 audio file from text using gTTS and returns it as a base64 string.
    
    Returns: A base64-encoded string of the MP3 data, or an empty string on failure.
    """
    try:
        # Create a TTS object (lang='fr' for French)
        tts = gTTS(text=text, lang='fr', slow=False)
        
        # Save the audio to a BytesIO object (in-memory file)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        # Encode the audio data to a base64 string
        audio_base64 = base64.b64encode(audio_fp.read()).decode('utf-8')
        return audio_base64
        
    except Exception as e:
        print(f"TTS Audio Generation Error: {e}")
        return ""
