#
# skk日本語変換ユーティリティ
#

# 定数の定義
SKK_DIC_FILE = "SKK-JISYO.M"

# 辞書のロード
# 引数:   skk辞書ファイルパス
# 戻り値: 正常時:辞書オブジェクト、異常時:None
#
def load_dic(dic_file=SKK_DIC_FILE):
    ssk_dic = dict()
    try:
        with  open(dic_file, mode="r", encoding="euc_jp") as dic_f:
            try:
                while  line := dic_f.readline():
                    if line[0:2]  != ";;":
                        key,kouho = line.split(" ")
                        ssk_dic[key] =  kouho.strip().split("/")[1:-1]
            except Exception as e:
                return None             
    except FileNotFoundError as err:
        return None
    return  ssk_dic 
