import json
import os
import re

def open_with_json(path):
    if os.path.exists(path):
        with open(path,'r', encoding="utf8") as file:
            data = json.load(file)
    else:
        data = {}
    return data

def clean_title(title):
    print(title)
    cleanString = re.sub('\W+',' ', title )
    cleanString = ' '.join([el for el in cleanString.split(' ') if el])
    return cleanString