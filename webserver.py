from flask import redirect,url_for,Flask,render_template, send_file, jsonify, request, make_response
from flask_cors import CORS, cross_origin
import os, json
from crawler_handler import call_crawler, get_title_crawler
import re

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def open_with_json(path):
    if os.path.exists(path):
        with open(path,'r') as file:
            data = json.load(file)
    else:
        data = {}
    return data

def get_site(url):
    if (url.startswith("https://mangatx.com/manga/")):
        return 'mangatx'

def add_follow_function(title, site, url):
    reading = open_with_json('ChapterList.json')
    #---- Add to the read.json with empty chapter
    if title in reading:
        # should be that it's followed on another site
        return
        reading[title]['sites'][site] = url
    else:
        reading[title] = {'sites':{site:url}, 'chapters': []}
    #---- Save to read.json
    with open('ChapterList.json', 'w') as file:
        json.dump(reading,file)
    #---- Call the crawler to get the list of chapters
    chapters, preview = call_crawler(site, title, url)
    chapters = [[chapter[0],chapter[1],False] for chapter in chapters]
    #---- add the list of chapters to the entire list of chapters
    data_local = open_with_json('chapterList.json')

    if title not in data_local:
        data_local[title] = {'sites':[{site:url}], 'chapters': chapters}
    else:
        for chapter in chapters:
            if not chapter in data_local[title]['chapters']:
                data_local[title]['chapters'].append(chapter)
    data_local[title]['preview'] = preview

    with open('chapterList.json', 'w') as file:
        json.dump(data_local, file)


def clean_title(title):
    cleanString = re.sub('\W+',' ', title )
    cleanString = ' '.join([el for el in cleanString.split(' ') if el])
    return cleanString

def save(url, title, site):
    data_local = open_with_json('chapterList.json')

    chapterName = data['chapterName']
    url = data['url']
    title = clean_title(data['title'])
    site = data['site']

    if title in data_local:
        if site in data_local[title]["sites"]:
            for i,chapter in enumerate(data_local[title]["chapters"]):
                if chapterName == chapter[0]:
                    data_local[title]["chapters"][i][2] = True
                    break

    with open('chapterList.json', 'w') as file:
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
    reading = open_with_json("chapterList.json")
    title = clean_title(data['title'])
    if reading: #check that reading is not empty
        if title in reading:
            if data['site'] in reading[title]['sites']:
                print(title)
                return jsonify({'followed':True})
    return jsonify({'followed':False})


@app.route('/API/follow', methods=['POST'])
def add_follow():
    data = request.get_json()
    title = clean_title(data['title'])
    add_follow_function(title, data['site'], data['url'])
    return "True"

@app.route('/API/get_read_list')
def send_read_list():
    list = open_with_json('chapterList.json')
    return jsonify([k for k in list])


@app.route('/')
def main():
    return redirect(url_for('display_list'))

@app.route('/API/get_preview/<string:title>')
def get_preview(title):
    chapter_list = open_with_json('chapterList.json')
    preview_name = chapter_list[title]['preview']
    return send_file(f"static/previews/{preview_name}")

@app.route('/API/get_infos_serie/<string:title>')
def get_infos_series(title):
    title = clean_title(title)
    chapter_list = open_with_json('chapterList.json')
    if title not in chapter_list:
        return jsonify('error')
    last_chap = chapter_list[title]['chapters'][-1]
    last_read = "None"
    for (i, chapter) in enumerate(chapter_list[title]['chapters']):
        if chapter[2]:
            last_read = "Some"
        if not chapter[2]:
            if i > 0:
                if chapter_list[title]['chapters'][i-1][2]:
                    last_read = chapter_list[title]['chapters'][i-1]
            break
    if last_read == "Some":
        last_read = chapter_list[title]['chapters'][-1]
    response = jsonify({'title':title, 'last_chapter':last_chap, 'last_chapter_read':last_read})
    return response


@app.route('/API/get_chap_list/<string:title>')
def get_chap_list(title):
    title = clean_title(title)
    chapter_list = open_with_json('chapterList.json')
    if title not in chapter_list:
        return jsonify('error')
    return jsonify(chapter_list[title]['chapters'])

@app.route('/API/add_serie/', methods=['POST','OPTION'])
def add_serie():
    data = request.get_json()
    url = data['url']
    site = get_site(url)
    title = clean_title(get_title_crawler(site, url))
    add_follow_function(title, site, url)

    res = make_response({'title':title})
    res.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    return res

@app.route('/API/read_until/', methods=['POST','OPTION'])
def add_read():
    data = request.get_json()
    title = clean_title(data['title'])
    chapter_name = data['chapter']
    data_local = open_with_json('chapterList.json')

    if title in data_local:
        for chapter in data_local[title]['chapters']:
            chapter[2] = True
            if chapter_name == chapter[0]:
                break

    with open('chapterList.json', 'w') as file:
        json.dump(data_local, file)

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    return res

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=4444)
