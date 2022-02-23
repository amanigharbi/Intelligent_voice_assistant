
import speech_recognition as sr
import pyttsx3 as tts
#from neuralintents import GenericAssistant
from TrainingModel import TrainingModel
import sys
import random
import json
import gtts
from playsound import playsound

recognizer = sr.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)  # rate is property, 150 is the value
voices = speaker.getProperty('voices')
with open('intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)



def choiseLang():
    recognizer = sr.Recognizer()
    while True:
        print('choose a language...')
        speaker.setProperty("voice", voices[-2].id)
        speaker.say("choose a language")
        speaker.runAndWait()
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                lang = recognizer.recognize_google(audio,language="fr-FR,ar-SA,en-US")
                lang = lang.lower()
                print(lang)
                if lang == "english" or lang == "anglais":
                    lang = "anglais"
                elif lang == "french" or lang == "français":
                    lang = "francais"
                elif lang == "arabic" or lang == "arabe":
                    lang = "arabe"
                else:
                    speaker.say("I'm sorry, can you repeat it again!")
                    speaker.runAndWait()
            return lang
        except sr.UnknownValueError:
            speaker.say("I'm sorry, try again!")
            speaker.runAndWait()

def execute(recognizer,pos,lang,msg):
    # Training a model to recognize the intents
    assistant = TrainingModel('intents.json')
    assistant.train_model()

    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio,language=lang)
                message = message.lower()
                print(message)
                reponse=assistant.request(message)
                print(reponse)
                speaker.setProperty("voice", voices[pos].id)
                speaker.say(reponse)
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.setProperty("voice", voices[pos].id)
            speaker.say(msg)
            speaker.runAndWait()


language = choiseLang()
print(language)
if language=="anglais":
    execute(recognizer,-2,"en-US","I'm sorry, can you repeat it again!")
if language=="francais":
    execute(recognizer,-3, "fr-FR", "Je ne comprend pas répéte s'il vous plait!")
if language=="arabe":
    execute(recognizer,-1,"ar-SA","لم افهم حاول مرة أخرى")