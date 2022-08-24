#update
#clone the chapterList
import shutil, os, json, requests
from crawler_handler import get_chapters_crawler

def open_with_json(path):
    if os.path.exists(path):
        with open(path,'r', encoding="utf8") as file:
            data = json.load(file)
    else:
        data = {}
    return data

shutil.copy('chapterList.json', 'chapterList_temp.json')
data_local = open_with_json("chapterList_temp.json")
series = data_local.keys()
for i,serie in enumerate(series):
    data_local = open_with_json("chapterList_temp.json")
    print(f"{i/len(series)*100} %",serie)
    try:
        change = False
        chapters = get_chapters_crawler(*list(data_local[serie]['sites'].items())[0])
        unpacked = [chapter[0] for chapter in data_local[serie]['chapters']]
        for chapter in chapters:
            if chapter[0] not in unpacked:
                change = True
                data_local[serie]['chapters'].append([*chapter, False])
        if change:
            with open('chapterList_temp.json','w') as file:
                json.dump(data_local, file)
    except Exception as err:
        print(err)
        
shutil.copy("chapterList_temp.json", "chapterList.json")
requests.get("http://127.0.0.1:5000/API/reload")