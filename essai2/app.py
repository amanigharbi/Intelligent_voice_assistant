from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from tensorflow.python.distribute.combinations import env
import chat
#from TrainingModel import TrainingModel
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
#assistant = TrainingModel('intents.json')
#assistant.train_model()
# print("train")
#assistant.save_model("VoiceBot")
@app.route("/")
def index_get():
    return render_template('base.html')

@app.post("/predict")
@cross_origin(origin='127.0.0.1')
def predict():
  
    #assistant.load_model("VoiceBot")
    text=request.get_json().get("message")
    #text="hello"
    print("text aaa", text)
    reponse = chat.response(text)
    print(reponse)
    return jsonify(reponse)


if __name__ == "__main__":
    app.run(debug=True,port=5050)

