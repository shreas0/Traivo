import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment
import os

engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    if len(voices) > 1:
        engine.setProperty("voice", voices[1].id)
except Exception as e:
    print("TTS initialization error:", repr(e))



def texttospeech(document, action="speak"):
    if engine is None:
        return "unavailable"

    if action == "stop":
        engine.stop()
        return "stopped"

    engine.say(document)
    engine.runAndWait()
    return "speaking"


def speechtotext():
    try:
        audio = AudioSegment.from_file("features/recordings/audio.webm")
        audio.export("features/recordings/audio.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("features/recordings/audio.wav") as source:
            audio = r.record(source)

        text = r.recognize_google(audio, language="en-IN")
    except Exception as e:
        print("STT error:", repr(e))
        text = ""

    for f in ["features/recordings/audio.webm", "features/recordings/audio.wav"]:
        if os.path.exists(f):
            os.remove(f)

    return text



