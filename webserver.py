from flask import redirect,url_for,Flask, send_file, jsonify, request, make_response
from flask_cors import CORS
import os, json
from crawler_handler import call_crawler, get_preview_crawler, get_title_crawler
import re, sys
import webbrowser
import time
from utils import open_with_json, clean_title
from chapterListHandler import Handler

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_site(url):
    if (url.startswith("https://mangatx.com/manga/")):
        return 'mangatx'
    elif (re.match("https:\/\/readmanganato\.com\/manga", url)):
        return "readmanganato"
    elif (re.match("https:\/\/mangakakalot\.com\/chapter", url)):
        return "mangakakalot"
    elif (re.match("https:\/\/asura\.nacm\.xyz\/.*-chapter-.*", url)):
        return "asurascans"
    else:
        return None


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
    handler.read_chapter(data)
    return "True"


@app.route('/API/followed', methods=["POST"])
def check_following():
    data = request.get_json()
    title = clean_title(data['title'])
    return jsonify({'followed': handler.following(title, data['site'])})


@app.route('/API/follow', methods=['POST'])
def add_follow():
    data = request.get_json()
    title = clean_title(data['title'])
    handler.add_follow(title, data['site'], data['url'])
    return "True"


@app.route('/API/get_read_list', methods=['GET','OPTION'])
def send_read_list():

    result = handler.get_read_list(request.args)

    res = make_response(jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@app.route('/')
def main():
    return redirect(url_for('display_list'))


@app.route('/API/get_preview/<string:title>')
def get_preview(title):
    preview_name = handler.get_preview(title)
    if os.path.exists(f"static/previews/{preview_name}"):
        return send_file(f"static/previews/{preview_name}")
    else:
        try:
            serie = handler.get_serie(title)
            get_preview_crawler(serie.sites[0],serie.title,serie.chapters[0].url)
            return send_file(f"static/previews/{preview_name}")
        except Exception as err:
            print(err)
            return send_file(f"static/previews/default.jpg")



@app.route('/API/get_infos_serie/<string:title>')
def get_infos_series(title):
    data = handler.get_serie(title).get_infos()
    return jsonify(data)


@app.route('/API/get_chap_list/<string:title>')
def get_chap_list(title):
    title = clean_title(title)
    serie = handler.get_serie(title)
    if not serie:
        return jsonify('error')
    return jsonify(serie.chapters_json())

@app.route('/API/add_site/', methods=['POST','OPTION'])
def add_site():
    data = request.get_json()
    handler.add_site(data['title'], data['site'])

    res = make_response({'title': data['title']})
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@app.route('/API/add_serie/', methods=['POST','OPTION'])
def add_serie():
    data = request.get_json()
    url = data['url']
    site = get_site(url)
    title = clean_title(get_title_crawler(site, url))
    handler.add_follow(title, site, url)

    res = make_response({'title':title})
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res

@app.route('/API/read_until/', methods=['POST','OPTION'])
def add_read():
    data = request.get_json()
    title = clean_title(data['title'])
    chapter_name = data['chapter']
    handler.read_until(title, chapter_name)

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res

@app.route('/API/open/', methods=['POST','OPTION'])
def open_url():
    data = request.get_json()
    url = data['url']

    webbrowser.open(url)

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res

@app.route('/API/update_chapter/', methods=['POST','OPTION'])
def update_chapter():
    handler.update()

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res

@app.route('/API/delete', methods=["POST",'OPTION'])
def del_serie():
    data = request.get_json()
    title = clean_title(data['title'])

    handler.delete(title)

    with open('logAction.txt','a') as file:
        file.write(f"delete {title}\n")

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res

@app.route('/API/drop', methods=["POST", 'OPTION'])
def drop_serie():
    data = request.get_json()
    title = clean_title(data['title'])
    handler.drop(title)

    with open('logAction.txt','a') as file:
        file.write(f"drop {title}\n")

    res = make_response()
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@app.route('/API/read', methods=["GET","POST"])
def is_read():
    name = clean_title(request.get_json()['title'])

    if handler.get_serie(name.lower(), True):
        return jsonify(1)
    return jsonify(0)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    sys.setrecursionlimit(100000)
    handler = Handler()
    if 'dev' in sys.argv:
        app.run(threaded=True, port=4444)
    else:
        from waitress import serve
        serve(app, host='127.0.0.1', port=4444)
