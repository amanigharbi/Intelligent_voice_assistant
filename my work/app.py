# importation des bibliotheques
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from tensorflow.python.distribute.combinations import env
from TrainingModel import TrainingModel
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
#declarer l assistant et faire l entrainement et sauvegarder le model
#assistant = TrainingModel('intents.json')
#assistant.train_model()
# print("train")
#assistant.save_model("VoiceBot")
@app.route("/")
def index_get():
    return render_template('base.html')

@app.post("/predict")
#@app.route("/predict", methods=['POST','GET'])
# @cross_origin(origin='127.0.0.1')
@cross_origin()
def predict():
  
    assistant.load_model("VoiceBot")
    text=request.get_json().get("message")
    print("text aaa", text)
    reponse = assistant.response(text)
    print(reponse)
    return jsonify(reponse)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5050)

