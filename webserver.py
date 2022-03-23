from flask import redirect,url_for,Flask,render_template, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import os, json

app = Flask(__name__)
cors = CORS(app)

def save(data):
    if os.path.exists('read.json'):
        with open('read.json', 'r') as file:
            data_local = json.load(file)
    else:
        data_local = {}

    for key, value in data.items():
        if key in data_local.keys():
            for link in value:
                if not link in data_local[key]:
                    data_local[key].append(link)
        else:
            data_local[key] = value
    with open('read.json', 'w') as file:
        json.dump(data_local, file)

def save_chapter_list(chapter_list):
    if os.path.exists('chapterLists.json'):
        with open('chapterLists.json', 'r') as file:
            data_local = json.load(file)
    else:
        data_local = {}

    for key, value in data.items():
        if key in data_local.keys():
            for link in value:
                if not link in data_local[key]:
                    data_local[key].append(link)
        else:
            data_local[key] = value
    with open('chapterLists.json', 'w') as file:
        json.dump(data_local, file)

@app.route("/API/uptime", methods=["GET"])
def is_up():
    return 'Yes'

@app.route("/API/synchro", methods=["POST"])
def check_synchro():
    data = request.get_json()
    return "True"

@app.route("/API/url", methods=["POST"])
def receive_url():
    data = request.get_json()
    print(data)
    trimed_data = {}
    trimed_data[data['title']] = [[data['chapterName'], data['url']]]
    save(trimed_data)
    return "True"

@app.route('/API/followed', methods=["POST"])
def check_following():
    data = request.get_json()
    if os.path.exists('read.json'):
        with open('read.json', 'r') as file:
            reading = json.load(file)
        if data['title'] in reading.keys():
            if data['site'] in reading[[data['title']]]['sites']:
                return jsonify({'followed':True})
        else:
            return jsonify({'followed':False})

@app.route('/API/follow', methods=['POST'])
def add_follow():
    data = request.get_json()
    print(data)

@app.route('/')
def main():
    return redirect(url_for('display_list'))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=4444)
