import datetime
import glob
import os
import time


def get_file_list(input_dir):
    # get the list of files in input directory.
    return sorted(
        [
            p
            for p in glob.glob(os.path.join(input_dir, "**"), recursive=True)
            if os.path.isfile(p)
        ]
    )


def get_all_url():
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
            and len(file_path.split("/")) == 5
        ):
            file_path = "/".join(file_path.split("/")[1:-1])
            res.append(main_url + file_path + "/")

    return res


import json

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

# Build the request body
url_list = get_all_url()

for url in url_list:
    content = {}
    content["url"] = url
    content["type"] = "URL_UPDATED"
    json_content = json.dumps(content)

    response, content = http.request(ENDPOINT, method="POST", body=json_content)
    result = json.loads(content.decode())
    dt_now = datetime.datetime.now()
    print(
        f"status : {response.status} | {dt_now.strftime('%Y-%m-%d %H:%M:%S')} | URL : {url}"
    )
    time.sleep(1.1)
