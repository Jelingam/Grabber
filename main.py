import requests
import json
import os


def merge_two_list(l1, l2):
    l3 = []
    ips_ports = []
    for item in l1:
        if item.strip():
            item = item.replace("/?POST%20", "").strip()
            ip_port = item.split("@")[1].split("#")[0]
            if not ip_port in ips_ports:
                ips_ports.append(ip_port)
                l3.append(item.strip())

        
    for item in l2:
        if item.strip():
            item = item.replace("/?POST%20", "").strip()
            ip_port = item.split("@")[1].split("#")[0]
            if not ip_port in ips_ports:
                ips_ports.append(ip_port)
                l3.append(item.strip())
    return list(set(l3))

def rename_configs(confs):
    renamed_config = []
    for conf in confs:
        conf = conf.strip()
        if conf.startswith("ss://"):
            ip = conf.split("@")[1].split("#")[0].split(":")[0]
            res = requests.get(f"https://api.iplocation.net/?ip={ip}")
            data = json.loads(res.text)
            c = data["country_code2"]
            name = f"{c} - {ip}"
            conf = conf.split("#")[0] + f"#{name}"
            renamed_config.append(conf)
    return renamed_config

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
        renamed_configs = rename_configs(merge_configs)
        
        with open(f"subs/detail/{name}.txt", "w") as f:
            for i, item in enumerate(renamed_configs):
                if i + 1 == len(renamed_configs):
                    f.write(f"{item}")
                else:
                    f.write(f"{item}\n")
    else:
        merge_configs = merge_two_list(new_configs, [])
        renamed_configs = rename_configs(merge_configs)
        with open(f"subs/detail/{name}.txt", "w") as f:
            for i, item in enumerate(renamed_configs):
                if i + 1 == len(renamed_configs):
                    f.write(f"{item}")
                else:
                    f.write(f"{item}\n")
        



        

    

