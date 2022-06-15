import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from flask import Flask, render_template, jsonify, request
import numpy as np
import matplotlib.pyplot as plt
from flask_cors import CORS
from flask_cors import cross_origin

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'application/json'
# with open('intents.json', 'r') as json_data:
#     intents = json.load(json_data)
# import our chat-bot intents file
data_file = open('intents_chat.json', encoding='utf-8').read()
intents = json.loads(data_file)
FILE = "data.pth" 
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def response(msg):
#     while True:
#     sentence = "do you use credit cards?"
#     sentence = input("You: ")
#     if sentence == "quit":
#         break

    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.1:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                ans=random.choice(intent['responses'])
                return ans;
                
#                 answer =random.choice(intent['responses'])
#                 print(f"{bot_name}: {random.choice(intent['responses'])}")
#     else:
#         print(f"{bot_name}: I do not understand...")
           
def chatbot_response(msg):
#     ints = predict_class(msg, model)
    res = response(msg)
    return res  
print(chatbot_response("ma7lolin lyoum?"))
bot_name = "Sam"
print("Let's chat! (type 'quit' to exit)")
app.static_folder = 'static'
# @app.route("/")
# def home():
#     return render_template("base.html")
@app.route("/get")
@cross_origin()
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

@app.route("/", methods=['GET'])
def index_get():
    return render_template("base.html")
@app.route('/predict', methods=["POST"])
@cross_origin(origin='127.0.0.1')
def chatbot_msg():
    if request.method == "POST":
        user_data = request.json

        text = user_data['message']
        response = chatbot_response(text)
        message = {"answer": response}
        return jsonify(message)
# @app.route("/predict", methods=['POST'])
# @cross_origin()
# def predict():
#     text = request.get_json().get("message")
#     response = chatbot_response(text)
#     message = {"answer": response}
#     return jsonify(message)
@app.route('/chatbot', methods=['GET'])
def chatbotResponse():
    reponse={}
#     if request.method == 'GET':
    userText = str(request.args['question'])
    answer =str(chatbot_response(userText))
    reponse['responses']= answer
    return reponse





if __name__ == '__main__':
#     http_server = WSGIServer(('', 5000), app)
#     http_server.serve_forever()
     app.run(host="0.0.0.0",debug=True)
