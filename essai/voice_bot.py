
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


# Greeting the user
def hello():
    for intent in intents['intents']:
        while intent['tag'] == "greeting":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-2].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break


def salutation():

    for intent in intents['intents']:
        while intent['tag'] == "salutation":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-3].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def التحية():
    for intent in intents['intents']:
        while intent['tag'] == "التحية":
            reponse = random.choice(intent['responses'])
            print(reponse)

            speaker.setProperty("voice", voices[-1].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break

def time():
    for intent in intents['intents']:
        while intent['tag'] == "Times":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-2].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def heure():
    for intent in intents['intents']:
        while intent['tag'] == "Heures":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-3].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def العمل():
    for intent in intents['intents']:
        while intent['tag'] == "اوقات العمل":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-1].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def OpenToday():
    for intent in intents['intents']:
        while intent['tag'] == "OpenToday":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-2].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def OuvertAujourdhui():
    for intent in intents['intents']:
        while intent['tag'] == "OuvertAujourdhui":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-3].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def thank():
    for intent in intents['intents']:
        while intent['tag'] == "Thank":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-2].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def Merci():
    for intent in intents['intents']:
        while intent['tag'] == "Merci":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-3].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def الشكر():
    for intent in intents['intents']:
        while intent['tag'] == "شكرا لك":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-1].id)
            speaker.say(reponse)
            speaker.runAndWait()
            break
# Exiting from your assistant
def close():
    for intent in intents['intents']:
        while intent['tag'] == "exit":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-2].id)
            speaker.say(reponse)
            speaker.runAndWait()
            sys.exit(0)
def exit():
    for intent in intents['intents']:
        while intent['tag'] == "Exit":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-3].id)
            speaker.say(reponse)
            speaker.runAndWait()
            sys.exit(0)

def المغادرة():
    for intent in intents['intents']:
        while intent['tag'] == "إلى اللقاء":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.setProperty("voice", voices[-1].id)
            speaker.say(reponse)
            speaker.runAndWait()
            sys.exit(0)
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
                lang = recognizer.recognize_google(audio,language="ar-SA,fr-FR,en-US")
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

def execute(recognizer,mappings,lang,msg):
    # Training a model to recognize the intents
    assistant = TrainingModel('intents.json', intent_methods=mappings)
    assistant.train_model()
    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio,language=lang)
                message = message.lower()
                print(message)
            assistant.request(message)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say(msg)
            speaker.runAndWait()


language = choiseLang()
print(language)
if language=="anglais":
    mappings = {
        "greeting": hello,
        "Times": time,
        "OpenToday": OpenToday,
        "Thank" : thank,
        "exit": close,

    }
    execute(recognizer,mappings,"en-US","I'm sorry, can you repeat it again!")

if language=="francais":
    mappings = {
        "salutation": salutation,
        "Heures": heure,
        "OuvertAujourdhui": OuvertAujourdhui,
        "Merci" : Merci,
        "Exit": exit,

    }
    execute(recognizer, mappings, "fr-FR", "Je ne comprend pas répéte s'il vous plait!")
if language=="arabe":
    mappings = {
        "التحية": التحية,
        "اوقات العمل": العمل,
         "شكرا لك" : الشكر,
        "إلى اللقاء" : المغادرة

    }

    execute(recognizer,mappings,"ar-SA","لم افهم حاول مرة أخرى")