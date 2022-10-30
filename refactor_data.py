from utils import open_with_json, save_with_json

data = open_with_json("chapterList.json")

for name,serie in enumerate(data):
    serie["sites"] = serie["sites"]