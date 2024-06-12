#
# カタカナ⇒ひらがな変換
#

import jaconv
import json

JSON_IN_FILE  = "data/romaji_dict.json"
JSON_OUT_FILE = "data/romaji_kana_dict.json"

new_data = ""
with open(JSON_IN_FILE, mode="r", encoding="utf-8") as f:
    while data := f.readline():
        new_data = new_data + jaconv.kata2hira(data)

print(new_data)
with open(JSON_OUT_FILE, mode="w", encoding="utf-8") as f:
    f.writelines(new_data)
