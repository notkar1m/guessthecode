import random,json,os
import requests as re
#curl -u 082ffb7023c7e8efb7a7:66c2ddf14c21bd6a440fbb6662321a7ae146f555 'https://api.github.com/user/repos'
with open("db/langs.json") as fp:
    langs_json = json.load(fp)
langs = langs_json
with open("db/codes.json") as fp:
    codes = json.load(fp)
def main():
    global codes
    url = f"https://api.github.com/gists/public?page={random.randint(0, 100)}"
    print(url)
    try:
        data = json.loads(re.get(str(url)).text)[0]['files']
        all_keys = []
        for i in data.keys():
            all_keys.append(i)
        r = random.randint(0, len(all_keys)-1)
        return {
            "lang":data[all_keys[r]]['language'],
            "code":data[all_keys[r]]['raw_url']
            }
    except KeyError:
        try:
            os.system("curl -u 082ffb7023c7e8efb7a7:66c2ddf14c21bd6a440fbb6662321a7ae146f555 'https://api.github.com/user/repos'")
            data = json.loads(re.get(str(url)).text)[0]['files']
            all_keys = []
            for i in data.keys():
                all_keys.append(i)
            r = random.randint(0, len(all_keys)-1)
            return {
                "lang":data[all_keys[r]]['language'],
                "code":data[all_keys[r]]['raw_url']
                }
        except KeyError:
            all_keys = []
            for i in codes:
                all_keys.append(i)
            r = random.randint(0, len(all_keys)-1)
            return codes[r]

    
def get():
    global codes
    x = main()
    while x["lang"] == None or x["lang"] == "Text" or x['lang'] == "Jupyter Notebook" or x['lang'] == "Markdown" or x['lang'] == "Public Key":
        x = main()
    if x['lang'] not in langs:
        langs.append(str(x['lang']))
        with open("db/langs.json", "w+") as fp:
            json.dump(langs, fp, indent=4)
    codes.append(x)
    with open("db/codes.json", "w+") as fp:
        json.dump(codes, fp, indent=4)
    print(x)
    return x