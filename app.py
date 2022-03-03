from flask import Flask, jsonify, request, render_template
import Spotify.spotif as spotif
import Spotify.spotify as spot
import requests
import json
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
    
    url = str("http://localhost:8080/languageclassifier/data/MUSIC/1d7c57f4-7f26-43e4-943d-c2d5fb72a01a")
    data = json.dumps( [  message_get, ])
    message_get =  requests.post(url, headers = { "accept": "application/json","Content-Type": "application/json"}, data=data )
    message_get = message_get.text[2:-2].lower()
    message_json = {
        "message": spot.sfind(message_get)
    }
    
    return jsonify(message_json)
 
if __name__ == "__main__":
    # spotify.PORT is 8081
    app.run(port = spotif.PORT)