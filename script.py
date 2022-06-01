from utils import open_with_json

data = open_with_json('chapterList.json')
for key in data.keys():
    if 'God' in key: print(key)

print(data['Tower Of God']['sites'])
