
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
with open('intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)
engine = tts.init()

for voice in engine.getProperty('voices'):
    print("aaaaaaaaa ",voice)


# Greeting the user
def hello():
    for intent in intents['intents']:
        while intent['tag'] == "greeting":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break


def salutation():

    for intent in intents['intents']:
        while intent['tag'] == "salutation":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def التحية():
    for intent in intents['intents']:
        while intent['tag'] == "التحية":
            reponse = random.choice(intent['responses'])
            print(reponse)
            t=gtts.gTTS(reponse,lang="ar")
            t.save("arabe.mp3")
            playsound("arabe.mp3")
            break

def time():
    for intent in intents['intents']:
        while intent['tag'] == "Times":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def heure():
    for intent in intents['intents']:
        while intent['tag'] == "Heures":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def العمل():
    for intent in intents['intents']:
        while intent['tag'] == "اوقات العمل":
            reponse = random.choice(intent['responses'])
            print(reponse)
            t=gtts.gTTS(reponse,lang="ar")
            t.save("arabe.mp3")
            playsound("arabe.mp3")
            break
def OpenToday():
    for intent in intents['intents']:
        while intent['tag'] == "OpenToday":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def OuvertAujourdhui():
    for intent in intents['intents']:
        while intent['tag'] == "OuvertAujourdhui":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def thank():
    for intent in intents['intents']:
        while intent['tag'] == "Thank":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def Merci():
    for intent in intents['intents']:
        while intent['tag'] == "Merci":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
def الشكر():
    for intent in intents['intents']:
        while intent['tag'] == "شكرا لك":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            break
# Exiting from your assistant
def close():
    for intent in intents['intents']:
        while intent['tag'] == "exit":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            sys.exit(0)
def exit():
    for intent in intents['intents']:
        while intent['tag'] == "Exit":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            sys.exit(0)

def المغادرة():
    for intent in intents['intents']:
        while intent['tag'] == "إلى اللقاء":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            sys.exit(0)
def choiseLang():
    recognizer = sr.Recognizer()
    try:
        print('choose a language...')
        speaker.say("choose a language")
        speaker.runAndWait()
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            lang = recognizer.recognize_google(audio,language="fr-FR,en-US,ar-AR")
            lang = lang.lower()
            print(lang)
            if lang == "english" or lang == "anglais":
                lang = "anglais"
            elif lang == "french" or lang == "francais":
                lang = "francais"
            elif lang == "arabic" or lang == "arabe":
                lang = "arabe"
            else:
                speaker.say("I'm sorry, can you repeat it again!")
                speaker.runAndWait()
        return lang
    except sr.UnknownValueError:
        speaker.say("I'm sorry, can you repeat it again!")
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

    # Training a model to recognize the intents
    assistant = TrainingModel('intents.json', intent_methods=mappings)
    assistant.train_model()
    # assistant.request()


    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio,language="en-US")
                message = message.lower()
                print(message)
            assistant.request(message)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I'm sorry, can you repeat it again!")
            speaker.runAndWait()
if language=="francais":
    mappings = {
        "salutation": salutation,
        "Heures": heure,
        "OuvertAujourdhui": OuvertAujourdhui,
        "Merci" : Merci,
        "Exit": exit,

    }

    # Training a model to recognize the intents
    assistant =TrainingModel('intents.json', intent_methods=mappings)
    assistant.train_model()
    # assistant.request()

    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio,language="fr-FR")
                message = message.lower()
                print(message)

            assistant.request(message)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("Je ne comprend pas répéte SVP!")
            speaker.runAndWait()
if language=="arabe":
    mappings = {
        "التحية": التحية,
        "اوقات العمل": العمل,
         "شكرا لك" : الشكر,
        "إلى اللقاء" : المغادرة


    }

    # Training a model to recognize the intents
    assistant = TrainingModel('intents.json', intent_methods=mappings)
    assistant.train_model()
    # assistant.request()


    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio,language="ar-QA")
                message = message.lower()
                print(message)
            assistant.request(message)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("لم افهم حاول مرة أخرى")
            speaker.runAndWait()