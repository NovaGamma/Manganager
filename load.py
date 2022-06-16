from utils import open_with_json
import os

#os.system("python update_script.py")

data = open_with_json('chapterList.json')

with open("logAction.txt",'r') as file:
    for line in file:
        line = line.rstrip('\n').split(' ')
        print(line)
        title = ' '.join(line[1:-1])
        if 'read' in line:
            pass
        elif 'readUntil' in line:
            pass
        elif 'delete' in line:
            pass
        elif 'add' in line:
            url = line[-1]
            pass
        elif 'addCrawler' in line:
            url = line[-1]
            pass
        else:
            print('Not recognised', line[0])
