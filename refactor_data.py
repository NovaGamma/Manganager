from utils import open_with_json, save_with_json

data = open_with_json("chapterList.json")

for name,serie in data.items():
    site, url = serie["sites"]
    if site == "readmanganato":
        splited = url.split("/")
        if splited[2] == "readmanganato.com":
            splited[2] = "chapmanganato.com"
        
        serie["sites"][1] = "/".join(splited)
        print(serie["sites"])

    if site == "asurascans":
        splited = url.split("/")
        if splited[2] == "www.asurascans.com":
            splited[2] = "asura.gg"
        
        serie["sites"][1] = "/".join(splited)
        print(serie["sites"])

save_with_json(data, "chapterList.json")