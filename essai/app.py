from flask import Flask, render_template, jsonify, request
import processor


app = Flask(__name__)

app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('base.html', **locals())



@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        # the_question = request.form['question']
        the_question =request.get_json().get("message")
        print("message "+the_question)

        response = processor.chatbot_response(the_question)
        print("reponse "+response)

    return jsonify(response)



if __name__ == '__main__':
    app.run(port='8888', debug=True)
