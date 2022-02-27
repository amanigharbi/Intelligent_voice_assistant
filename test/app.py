from flask import Flask, render_template, request, redirect, jsonify
import speech_recognition as sr
import json
from neuralintents import GenericAssistant

from chat import  TrainingModel

app = Flask(__name__)


@app.route("/")
def index_get():



    return render_template('base.html')

@app.post("/predict")
def predict():
    assistant = TrainingModel('intents.json')
    assistant.train_model()
    text=request.get_json().get("message")
    print("text aaa", text)
    reponse = assistant.request1(text)
    message={"answer": reponse}
    return jsonify(message)
if __name__ == "__main__":
    app.run(debug=True)

