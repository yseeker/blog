import csv  # モジュール"CSV"の呼び出し

from bs4 import BeautifulSoup

# スクレイピング対象のhtmlファイルからsoupを作成
soup = BeautifulSoup(open(path), "html.parser")

links = soup.find_all("meta")  # 全てのaタグ要素を取得

csvlist = []  # 配列を作成

for link in links:  # aタグのテキストデータを配列に格納
    sample_txt = link.content
    print(sample_txt)
