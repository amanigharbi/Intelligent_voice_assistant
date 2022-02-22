from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import sys
import json
import nltk
from gtts import gTTS
recognizer = sr.Recognizer()
speaker = tts.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)

with open('intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)
    print("ok")
def talk(text):
    speaker.say(text)
    speaker.runAndWait()
def take_command():

    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = recognizer.listen(source)
            command = recognizer.recognize_google(voice)
            command = command.lower()
           # if 'bob' in command:
            #    command = command.replace('alexa', '')
             #   print(command)
    except sr.UnknownValueError:
        command = sr.Recognizer()

    return command
words = []
def hello():
    speaker.say("Hello. What can I do for you?")
    speaker.runAndWait()
def run_alexa():
    command = take_command()
    print(command)

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            words.append(pattern)
    for i in range(len(words)):
        if command in words[i]:
            print("yeeey")
        else:
            print("ooooo")











while True:
    run_alexa()