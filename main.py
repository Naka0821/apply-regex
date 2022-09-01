import csv
import requests
from bs4 import BeautifulSoup as bs
import re

# サイト内のページを見る個数
MAX_ROOP = 3
# かける正規表現
patterns = ["いかがでしたか","いかがでしょうか"]

def parse_list(list, flag):
    for pt in patterns:
        flag[pt] = False
    for i, el in enumerate(list):
        if i >= MAX_ROOP:
            break
        print(el)
        text = get_text(el)
        for pattern in patterns:
            if flag[pattern]:# たっているフラグは無視
                continue
            else:               # たっていないフラグのみ正規表現をかける
                try:
                    if re.search(pattern, text):
                        flag[pattern] = True
                except Exception:
                    continue
    print(flag)
    print("*************************** one list finish *************************")
    return flag

def get_text(url):
    if re.match("http.*", url):
        try:
            html = requests.get(url).text
            soup = bs(html, "html.parser")
        except Exception:
            return
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        #lines= [line.strip() for line in text.splitlines()]
        #text="\n".join(line for line in lines if line)
        #print(text)
        return text

def apply_regex(csv_file):
    dict = {}
    for i, row in enumerate(csv_file):
        append = {}
        append = parse_list(row, append)
        dict[i] = append
        
    return dict

if __name__ == "__main__":
    csv.field_size_limit(1000000000)
    with open("url.csv", encoding="utf-8") as urlcsv:
        reader = csv.reader(urlcsv)
        dict = apply_regex(reader)
        print(dict)