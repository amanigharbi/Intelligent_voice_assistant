from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import pyttsx3 as tts
#from neuralintents import GenericAssistant
from gtts import gTTS


from TrainingModel import TrainingModel
import sys
import random
import json
import playsound

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
            speaker.say(reponse)
            speaker.runAndWait()
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
            speaker.say(reponse)
            speaker.runAndWait()
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
    print('choose a language...')
    speaker.setProperty("voice", voices[-2].id)
    speaker.say("choose a language")
    speaker.runAndWait()
    while True:
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

#assistant = TrainingModel('intents.json')
#assistant.train_model()
#print("train")
#assistant.save_model("VoiceBot")
#print("ok")
def prepare(recognizer,mappings,pos,lang,msg):
    # Training a model to recognize the intents
    assistant = TrainingModel('intents.json', intent_methods=mappings)
    assistant.load_model("VoiceBot")
    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio,language=lang)
                message = message.lower()
                print(message)
                reponse=assistant.request1(message)
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
    mappings = {
        "greeting": hello,
        "Times": time,
        "OpenToday": OpenToday,
        "Thank" : thank,
        "exit": close,

    }
    prepare(recognizer,mappings,-2,"en-US","I'm sorry, can you repeat it again!")
if language=="francais":
    mappings = {
        "salutation": salutation,
        "Heures": heure,
        "OuvertAujourdhui": OuvertAujourdhui,
        "Merci" : Merci,
        "Exit": exit,

    }
    prepare(recognizer,mappings,-3, "fr-FR", "Je ne comprend pas répéte s'il vous plait!")
if language=="arabe":
    mappings = {
        "التحية": التحية,
        "اوقات العمل": العمل,
         "شكرا لك" : الشكر,
        "إلى اللقاء" : المغادرة


    }

    prepare(recognizer,mappings,-1,"ar-SA","لم افهم حاول مرة أخرى")


