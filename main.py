import requests
import json
import os

def merge_two_list(l1, l2):
    l3 = []
    for item in l1:
        if item.strip():
            l3.append(item)
        
    for item in l2:
        if item.strip():
            l3.append(item)
    
    return list(set(l3))


with open("url.json") as f:
    alldata  = json.load(f)

allowable_types = ["mixed", "base64", "clash", "hiddify", "nika", "v2ray"]

new_configs = []
for sub in alldata["subs"]:
    urls = []
    if isinstance(sub["url"], str):
        urls.append(sub["url"])
    if isinstance(sub["url"], list):
        for u in sub["url"]:
            urls.append(u)
    for url in urls:
        if not url.startswith("https"):
            url = "https://" + url
        res = requests.get(url)
        text = res.text
        confs = text.splitlines()
        for item in confs:
            if item.strip():
                new_configs.append(item.strip())
    name = sub.get("name")
    if os.path.isfile(f"subs/detail/{name}.txt"):
        with open(f"subs/detail/{name}.txt") as f:
            old_configs = f.readlines()
        merge_configs = merge_two_list(new_configs, old_configs)
        
        with open(f"subs/detail/{name}.txt", "w") as f:
            for i, item in enumerate(merge_configs):
                if i + 1 == len(merge_configs):
                    f.write(f"{item}")
                else:
                    f.write(f"{item}\n")
    else:
        merge_configs = merge_two_list(new_configs, [])
        with open(f"subs/detail/{name}.txt", "w") as f:
            for i, item in enumerate(merge_configs):
                if i + 1 == len(merge_configs):
                    f.write(f"{item}")
                else:
                    f.write(f"{item}\n")
        



        

    

