import csv
import requests
from bs4 import BeautifulSoup as bs
import re

# サイト内のページを見る個数
MAX_ROOP = 3
# かける正規表現のリスト
patterns = ["いかがでしたか","いかがでしょうか"]

def parse_list(list):
    flag = {}
    for pt in patterns:             # 初期値設定
        flag[pt] = False
    for i, el in enumerate(list):   # リストの各要素(URL)毎に処理
        if i >= MAX_ROOP:           # ループ回数の監視
            break
        text = get_text(el)         # BSでテキストのみスクレイピング
        for pattern in patterns:    # 正規表現リストから各パターンを読み込んで処理
            if flag[pattern]:   # たっているフラグは無視
                continue
            else:               # たっていないフラグのみ正規表現をかける
                try:
                    if re.search(pattern, text):
                        flag[pattern] = True
                except Exception:
                    continue
    return flag

def get_text(url):
    try:
        html = requests.get(url).text
    except Exception:
        return
    soup = bs(html, "html.parser")
    for script in soup(["script", "style"]):    # スクリプトとスタイルの除外
        script.decompose()
    text = soup.get_text()                      # テキストの取得
    return text

def apply_regex(csv_file):                  # csvを引数に受け取り
    dict = {}
    for i, row in enumerate(csv_file):      # 行毎の処理(サイト毎の処理)
        append = parse_list(row)    
        dict[i] = append                    # {id: {pattern: bool, pattern: bool, ...}, id: {...}, ...}
                                            # id:int pattern:str bool:bool
    return dict

if __name__ == "__main__":
    csv.field_size_limit(1000000000)
    with open("url.csv", encoding="utf-8") as urlcsv:
        reader = csv.reader(urlcsv)
        dict = apply_regex(reader)
        print(dict)