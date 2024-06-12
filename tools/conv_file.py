# skkバイナリ辞書データファイルの作成

import skk
import struct

# 定数
SSK_BINDIC_FILE = "ssk_dic_m.bin"

# skk辞書のロード
dic = skk.load_dic()

# 辞書データをキーワードでソート
new_dic = sorted(dic.items())

keyword_index = bytearray()
keyword_data = bytearray()

# キーワードインデックス、キーワードデータの作成
for key, kouho in new_dic:
    # インデックスの格納
    addr = len(keyword_data)
    keyword_index.extend(struct.pack("<L", addr))

    # キーワードの格納
    keyword_data.extend(key.encode("utf-8"))
    keyword_data.append(ord(","))
    
    # 候補データの格納
    for word in kouho:
        keyword_data.extend(word.encode("utf-8"))
        keyword_data.append((ord(",")))

# ヘッダー情報
size_keyword = len(new_dic)     # キーワード数
keyword_index_top  = 12         # インデックス部先頭アドレス  
keyword_data_top = keyword_index_top + len(keyword_index)  # キーワードデータ先頭アドレス

# インデックスとキーワードデータの結合
skk_bin_data = bytearray()
skk_bin_data.extend(struct.pack("<L", size_keyword))
skk_bin_data.extend(struct.pack("<L", keyword_index_top))
skk_bin_data.extend(struct.pack("<L", keyword_data_top))
skk_bin_data.extend(keyword_index)
skk_bin_data.extend(keyword_data)

# データをファイルに書き込み
try:
    with open(SSK_BINDIC_FILE,  mode="wb") as of:
        of.write(skk_bin_data)
except Exception as e:
    print("File error",  e)




