
import pyttsx3 as tts

engine = tts.init()

for voice in engine.getProperty('voices'):
    print("aaaaaaaaa " ,voice)


voices = engine.getProperty('voices')
print("bbbbbb",voices[-2].id)
engine.setProperty("voice", voices[-2].id)
engine.say("مرحبًا بالعالم")
engine.runAndWait()
'''
engine.say('hello world')
engine.say("مرحبًا بالعالم")
engine.runAndWait()
'''