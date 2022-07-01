from utils import open_with_json, clean_title
from webserver import get_infos_function

data = open_with_json('chapterList.json')


total = 0
for title in data.keys():
    infos = get_infos_function(title)  
    n = data[title]['chapters'].index(infos['last_chapter_read'])
    total += n

print(total)
input('stop')

logs = []

for title in data.keys():
    infos = get_infos_function(title)  
    logs.append(f"add {title} {data[title]['sites'][infos['site']]}")
    logs.append(f"addCrawler {title} {data[title]['sites'][infos['site']]}")
    logs.append(f"readUntil {title} {data[title]['chapters'].index(infos['last_chapter_read'])}")
    if infos['state'] == 'dropped':
        logs.append(f"drop {title}")

with open("test.txt",'w') as file:
    print("\n".join(logs),file=file)