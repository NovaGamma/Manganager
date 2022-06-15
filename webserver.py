from flask import redirect,url_for,Flask,render_template, send_file, jsonify, request, make_response
from flask_cors import CORS, cross_origin
import os, json
from crawler_handler import call_crawler, get_title_crawler, get_chapters_crawler
import re, shutil, subprocess, sys
import webbrowser
import time
from utils import open_with_json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_site(url):
    if (url.startswith("https://mangatx.com/manga/")):
        return 'mangatx'
    elif (re.match("https:\/\/readmanganato\.com\/manga.+", url)):
        return "readmanganato"

def get_infos_function(title, chapter_list = ''):
    title = clean_title(title)
    if chapter_list == '':
        chapter_list = open_with_json('chapterList.json')
    if title not in chapter_list:
        return 'error'
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
    return {'title':title,
            'last_chapter':last_chap,
            'last_chapter_read':last_read,
            'site':list(chapter_list[title]['sites'].keys())[0],
            'date':chapter_list[title]['date'],
            'state':chapter_list[title]['state']
            }

def add_follow_function(title, site, url):
    reading = open_with_json('ChapterList.json')
    #---- Add to the read.json with empty chapter
    if title in reading:
        # should be that it's followed on another site
        return
        reading[title]['sites'][site] = url
    else:
        reading[title] = {'sites':{site:url}, 'chapters': [], 'date':time.time(), 'state':'reading'}
    #---- Save to read.json
    with open('chapterList.json', 'w') as file:
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

def save(data):
    data_local = open_with_json('chapterList.json')

    chapterName = data['chapterName']
    url = data['url']
    title = clean_title(data['title'])
    site = data['site']

    if title in data_local:
        if site in data_local[title]["sites"]:
            data_local[title]['date'] = time.time()
            for i,chapter in enumerate(data_local[title]["chapters"]):
                if chapterName == chapter[0]:
                    data_local[title]["chapters"][i][2] = True
                    print(data)
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
    save(data)
    return "True"


@app.route('/API/followed', methods=["POST"])
def check_following():
    data = request.get_json()
    reading = open_with_json("chapterList.json")
    title = clean_title(data['title'])
    print(title)
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


@app.route('/API/get_read_list', methods=['GET','OPTION'])
def send_read_list():
    chapterList = open_with_json('chapterList.json')
    not_finished = request.args['not_finished']
    if not_finished == "true":
        not_finished = True
    else:
        not_finished = False
    print(not_finished)
    #----------- filter chapterList to remove dropped

    chapterList = {serie:chapterList[serie] for serie in chapterList.keys() if chapterList[serie]['state'] != "dropped"}

    result = []
    for k in list(chapterList.keys()):
        infos = get_infos_function(k, chapterList)
        if not_finished and infos['last_chapter'] != infos['last_chapter_read'] or not not_finished:
            result.append({**infos, "isFinished":infos['last_chapter'] == infos['last_chapter_read']})

    #---- sort result by date
    #result.sort(key=lambda x: x.get('date'), reverse=True)
    def ratio(x):
        serie = chapterList[x.get('title')]
        last_chap = x.get("last_chapter_read")
        if last_chap == 'None':
            index = 0
        else:
            index = serie['chapters'].index(last_chap)
        return (index+1)/len(serie['chapters'])
        
    result.sort(key=ratio)

    res = make_response(jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    return res


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
    data = get_infos_function(title)
    return jsonify(data)


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

@app.route('/API/open/', methods=['POST','OPTION'])
def open_url():
    data = request.get_json()
    url = data['url']

    webbrowser.open(url)

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    return res

@app.route('/API/update_chapter/', methods=['POST','OPTION'])
def update_chapter():
    current_time = time.time()
    log = open_with_json('log.json')
    update_time = log['update']
    if current_time - update_time > 86000:
        os.system("python update_script.py")
        log['update'] = time.time()
        with open('log.json', 'w') as file:
            json.dump(log, file)

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    return res

@app.route('/API/delete', methods=["POST",'OPTION'])
def del_serie():
    data = request.get_json()
    title = clean_title(data['title'])
    data_local = open_with_json('chapterList.json')

    if title in data_local.keys():
        del data_local[title]

    with open('chapterList.json','w') as file:
        json.dump(data_local, file)

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    return res


@app.route('/API/read', methods=["GET","POST"])
def is_read():
    name = clean_title(request.get_json()['title'])
    data = open_with_json('chapterList.json')

    if name.lower() in  [k.lower() for k in data.keys()]:
        return jsonify(1)
    return jsonify(0)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    print(sys.argv)
    if 'dev' in sys.argv:
        app.run(threaded=True, port=4444)
    else:
        from waitress import serve
        serve(app, host='127.0.0.1', port=4444)
