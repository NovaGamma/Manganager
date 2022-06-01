import json
import os

def open_with_json(path):
    if os.path.exists(path):
        with open(path,'r', encoding="utf8") as file:
            data = json.load(file)
    else:
        data = {}
    return data
