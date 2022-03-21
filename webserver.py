from flask import redirect,url_for,Flask,render_template, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import os, json

app = Flask(__name__)
cors = CORS(app)

@app.route("/API/uptime", methods=["GET"])
def is_up():
    return 'Yes'

@app.route("/API/synchro", methods=["POST"])
def check_synchro():
    return "True"

@app.route("/API/url", methods=["POST"])
def receive_url():
    data = request.get_json()
    print(data['url'])
    return "True"

@app.route('/')
def main():
    return redirect(url_for('display_list'))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=4444)
