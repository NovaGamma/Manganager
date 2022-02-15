from asyncio import subprocess
from unittest import result
from urllib import *
from urllib import request
from flask import Flask
from json import *

@app.route("/request", methods=["POST"]):
def get_request():
    data = request.get_json()
    print(data)
    '''
    url = data['url']
    for site in sites:
        if url.startswith(site):
            path = url
            website = site
    cmd += path
    subprocess.call(cmd, shell=True)'''
    return 'ok' #if len(result) == 1 else 'Error'

@app.route('/url_check', methods=["POST"]
def check_url():
    url = request.get_json()['url']
    for site in sites:
        if url.startswith(site):
            ret = 'Ok'
        else
            ret = 'No'
    return jsonify(ret)
