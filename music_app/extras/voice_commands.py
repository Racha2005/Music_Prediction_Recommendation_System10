
"""
voice_commands.py
Simple voice command wrapper using SpeechRecognition (recognizes single phrase from microphone).
Requires microphone and SpeechRecognition + a recognizer (Google API used by default).
Usage:
    python music_app/extras/voice_commands.py
"""
def listen_once():
    try:
        import speech_recognition as sr
    except Exception:
        print("speech_recognition not installed. Install with: pip install SpeechRecognition")
        return None
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say a command...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except Exception as e:
        print("Could not transcribe:", e)
        return None

if __name__ == "__main__":
    listen_once()
