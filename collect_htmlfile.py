import datetime
import glob
import json
import os
import time

import httplib2
from oauth2client.service_account import ServiceAccountCredentials

JSON_KEY_FILE = "client_secrets.json"

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


# Authorize credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    JSON_KEY_FILE, scopes=SCOPES
)
http = credentials.authorize(httplib2.Http())


def get_file_list(input_dir):
    # get the list of files in input directory.
    return sorted(
        [
            p
            for p in glob.glob(os.path.join(input_dir, "**"), recursive=True)
            if os.path.isfile(p)
        ]
    )


def get_all_file_path():
    file_list = get_file_list("docs/posts")
    main_url = "https://www.yusaito.com/blog/"
    tgt = []

    # check_latest_update
    for file_path in file_list:
        tgt.append((file_path, os.path.getctime(file_path)))

    sorted_file_list_with_timestamp = sorted(tgt, key=lambda x: -x[1])

    res = []

    for file_path, _ in sorted_file_list_with_timestamp:
        if (
            not ("page" in file_path or ".png" in file_path or ".jpg" in file_path)
            and len(file_path.split("/")) >= 5
        ):
            res.append(file_path)

    return res


from bs4 import BeautifulSoup


# スクレイピング対象のhtmlファイルからsoupを作成
def check_noindex(html_path):
    soup = BeautifulSoup(open(html_path), "html.parser")

    links = soup.find_all("meta")  # 全てのaタグ要素を取得# 配列を作成

    return len(links) != 3  # aタグのテキストデータを配列に格納


file_path_list = get_all_file_path()
xml_list = set()
for file_path in file_path_list:
    if file_path.split(".")[-1] == "xml":
        xml_list.add(file_path[:-3])
html_list = []
for file_path in file_path_list:
    if file_path.split(".")[-1] == "html":
        html_list.append(file_path)

correct_html_list = []
for file_path in html_list:
    if file_path[:-4] not in xml_list:
        correct_html_list.append(file_path)

for path in correct_html_list:
    check_noindex(path)

url_list = []
main_url = "https://www.yusaito.com/blog/"
for file_path in correct_html_list:
    if check_noindex(file_path):
        file_path = "/".join(file_path.split("/")[1:-1])
        url_list.append(main_url + file_path + "/")

print(f"total number of URLs : {len(url_list)}")

print(url_list[25])
# for url in url_list:
#     content = {}
#     content["url"] = url
#     content["type"] = "URL_UPDATED"
#     json_content = json.dumps(content)

#     response, content = http.request(ENDPOINT, method="POST", body=json_content)
#     result = json.loads(content.decode())
#     dt_now = datetime.datetime.now()
#     print(
#         f"status : {response.status} | {dt_now.strftime('%Y-%m-%d %H:%M:%S')} | URL : {url}"
#     )
#     time.sleep(1.1)
