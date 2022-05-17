from flask import redirect,url_for,Flask,render_template, send_file, jsonify, request
from flask_cors import CORS, cross_origin
import os, json
from crawler_handler import call_crawler


app = Flask(__name__)
cors = CORS(app)

def open_with_json(path):
    if os.path.exists(path):
        with open(path,'r') as file:
            data = json.load(file)
    else:
        data = {}
    return data


def save(data):
    data_local = open_with_json('read.json')

    chapterName = data['chapterName']
    url = data['url']
    title = data['title']

    if title in data_local:
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
    reading = open_with_json('read.json')
    if reading: #check that reading is not empty
        if data['title'] in reading:
            if data['site'] in reading[[data['title']]]['sites']:
                return jsonify({'followed':True})
    return jsonify({'followed':False})


@app.route('/API/follow', methods=['POST'])
def add_follow():
    data = request.get_json()

    reading = open_with_json('read.json')
    #---- Add to the read.json with empty chapter
    if data['title'] in reading:
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
    data_local = open_with_json('chapterList.json')

    if data['title'] not in data_local:
        data_local['title'] = {'sites':[{data['site']:data['url']}], 'chapters': chapters}
    else:
        for chapter in chapters:
            if not chapter in data_local['title']['chapters']:
                data_local['title']['chapters'].append(chapter)

    with open('chapterList.json', 'w') as file:
        json.dump(data_local, file)

    return "True"

@app.route('/API/get_read_list')
def send_read_list():
    list = open_with_json('read.json')
    return jsonify(list)

@app.route('/API/get_chapters_list')
def send_chapters_list():
    list = open_with_json('chapterList.json')
    return jsonify(list)

@app.route('/')
def main():
    return redirect(url_for('display_list'))


@app.route('/API/get_infos_serie', methods = ['POST'])
def get_infos_series(): 
    data = request.get_json()
    title = data.title
    chapter_list = open_with_json('chapterList.json')
    if title not in chapter_list: 
        return jsonify('error')
    image = chapter_list[title]['preview']
    last_chap = chapter_list[title]['chapters'][-1]
    for (i, chapter) in enumerate(chapter_list[title]['chapters']): 
        if not chapter[2]: 
            if i == 0: 
                last_read = None
            else: 
                last_read = chapter_list[title]['chapters'][i-1]
            break
    return jsonify(image, last_chap, last_read)


@app.route('/API/get_chap_list', methods = ['POST'])
def get_chap_list(): 
    data = request.get_json()
    title = data.title
    chapter_list = open_with_json('chapterList.json')
    if title not in chapter_list: 
        return jsonify('error')
    return jsonify(chapter_list[title]['chapters'])




if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=4444)
