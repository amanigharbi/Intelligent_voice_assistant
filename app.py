from flask import Flask, render_template, request, jsonify
# from gtts import gTTS
from TrainingModel import TrainingModel
app = Flask(__name__)

assistant = TrainingModel('intents.json')
# assistant.train_model()
# print("train")
# assistant.save_model("VoiceBot")
@app.route("/")
def index_get():


    return render_template('base.html')
@app.post("/predict")
def predict():
  
    assistant.load_model("VoiceBot")
    text=request.get_json().get("message")
    print("text aaa", text)
    # tts = gTTS(text)
    # tts.save('message.mp3')
    reponse = assistant.response(text)
    print(reponse)
    return jsonify(reponse)


if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port=5050)

