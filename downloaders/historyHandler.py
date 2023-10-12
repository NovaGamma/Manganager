import os
import json

def get_history():
    try:
        file = open('history.json')
        return json.load(file)
    except FileNotFoundError:
        return {}

def add_to_history(name, number):
    history = get_history()
    if name in history.keys():
        if float(number) > float(history[name]):
            history[name] = number
    else:
        history[name] = number

    with open('history.json','w') as file:
        json.dump(history, file)
