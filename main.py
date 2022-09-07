import csv
from types import NoneType
import requests
from bs4 import BeautifulSoup as bs
import re

# サイト内のページを見る個数
MAX_ROOP = 20
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
        if type(text) == NoneType:  # 取得失敗の場合次へ
            continue
        for pattern in patterns:    # 正規表現リストから各パターンを読み込んで処理
            if flag[pattern]:       # たっているフラグは無視
                continue
            else:                   # たっていないフラグのみ正規表現をかける
                cmp = re.compile(pattern)
                try:
                    if cmp.search(text):
                        flag[pattern] = True
                except:
                    continue
    return flag

def get_text(url):
    try:
        html = requests.get(url, timeout=5.0).text
    except:
        return
    soup = bs(html, "html.parser")
    text = soup.get_text(strip=True)                      # テキストの取得
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