from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import json

from essai.voice_bot import execute

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    recognizer = sr.Recognizer()

    if request.method == "POST":
        print("FORM DATA RECEIVED")
        print()


    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

