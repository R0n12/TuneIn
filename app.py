from flask import Flask, jsonify, request, render_template
from spotify import spotify

app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/user_input', methods=['GET'])
def user_input():
    global message_get
    message_get = ""

    message_get = request.args['message']
    print("Receive frontend info %s" % message_get)
    print("Receive frontend info type is " + str(type(message_get)))

    return "Get music genre successfully"

@app.route('/change_to_json', methods=['GET'])
def change_to_json():

    global message_get
    message_json = {
        "message": message_get
    }

    return jsonify(message_json)
 
if __name__ == "__main__":
    # spotify.PORT is 8081
    app.run(port = spotify.PORT)