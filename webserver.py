from flask import redirect,url_for,Flask,render_template, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import os, json
from crawler_handler import call_crawler


app = Flask(__name__)
cors = CORS(app)


def save(data):
    if os.path.exists('read.json'):
        with open('read.json', 'r') as file:
            data_local = json.load(file)
    else:
        data_local = {}

    chapterName = data['chapterName']
    url = data['url']
    title = data['title']

    if title in data_local.keys():
        if not (chapterName, url) in data_local[title]['chapters']:
            data_local[title]['chapters'].append((chapterName, url))
    else:
        data_local[title] = {'sites':[site], 'chapters':[(chapterName, url)]}

    with open('read.json', 'w') as file:
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
    save(data)
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
        return jsonify({'followed':False})


@app.route('/API/follow', methods=['POST'])
def add_follow():
    data = request.get_json()

    if os.path.exists('read.json'):
    #---- Add to the read.json with empty chapter
        with open('read.json', 'r') as file:
            reading = json.load(file)
    else:
        reading = {}
    if data['title'] in reading.keys():
        # should be that it's followed on another site
        reading[data['title']]['sites'].append({data['site']:data['url']})
    else:
        reading[data['title']] = {'sites':[{data['site']:data['url']}], 'chapters': []}
    #---- Save to read.json
    with open('read.json', 'w') as file:
        json.dump(reading,file)
    #---- Call the crawler to get the list of chapters
    chapters = call_crawler(data['site'], data['title'], data['url'])

    #---- add the list of chapters to the entire list of chapters
    if os.path.exists('chapterList.json'):
        with open('chapterList.json', 'r') as file:
            data_local = json.load(file)
    else:
        data_local = {}

    if data['title'] not in data_local.keys():
        data_local['title'] = {'sites':[{data['site']:data['url']}], 'chapters': chapters}
    else:
        for chapter in chapters:
            if not chapter in data_local['title']['chapters']:
                data_local['title']['chapters'].append(chapter)

    with open('chapterList.json', 'w') as file:
        json.dump(data_local, file)

    return "True"

@app.route('/')
def main():
    return redirect(url_for('display_list'))


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=4444)
