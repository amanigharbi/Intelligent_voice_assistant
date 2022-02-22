import speech_recognition
import pyttsx3 as tts
from neuralintents import GenericAssistant
import sys
import random
import json



recognizer = speech_recognition.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)  # rate is property, 150 is the value
# Creating an object to access the todo list
todo_list = ['Go Shopping', 'Clean Room']
with open('intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)


def talk(text):
    speaker.say(text)
    speaker.runAndWait()


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
    speaker.say("Salut, comment puis_je vous aider?")
    speaker.runAndWait()


def time():
    for intent in intents['intents']:
        while intent['tag'] == "Times":
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



# Exiting from your assistant
def close():
    for intent in intents['intents']:
        while intent['tag'] == "exit":
            reponse = random.choice(intent['responses'])
            print(reponse)
            speaker.say(reponse)
            speaker.runAndWait()
            sys.exit(0)




mappings = {
    "greeting": hello,
    "Times": time,
    "OpenToday": OpenToday,
    "exit": close,

}

# Training a model to recognize the intents
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()
# assistant.request()


while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()
            print(message)
        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
