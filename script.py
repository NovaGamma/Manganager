from utils import open_with_json

data = open_with_json('chapterList.json')


print(data['Return of the Frozen Player']['date'])
