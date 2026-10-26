import pyttsx3
import speech_recognition as sr
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)

r = sr.Recognizer()
r.pause_threshold = 0.8


def texttospeech(document):
    text=engine.say(str(document))
    engine.runAndWait()
    return



def texttospeech(document):
    engine=pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[1].id)
    engine.say(document)
    engine.runAndWait()
    return 

def speechtotext():

    
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Couldn't understand"
    except sr.RequestError:
        return "engine is not online"


#for test
#texttospeech("Hi, my name is siri and i want to describe my project right now")
#print(speechtotext())