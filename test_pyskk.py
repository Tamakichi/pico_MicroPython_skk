import sys
if sys.implementation.name == 'cpython':
    sys.path.append("./lib")
from pyskk import pyskk

skk = pyskk.skk()
skk.begin()
print("キーワード数:", skk.len())

while True:
    token = input("ローマ字入力(end='@'):")
    if token == "@":
        skk.end()
        sys.exit()
    menu = input("[0:無変換 1:ひらがな 2:カタカナ 3:変換 4:取り消し]:")

    # 無変換
    if menu == "0":
        word = token
        print("確定=", word)
        continue
    # ひらがな
    elif menu == "1":
        word = skk.to_hiragana(token)
        print("確定=", word)
        continue
    # カタカナ
    elif menu == "2":        
        word = skk.to_katakana(token)
        print("確定=", word)
        continue
    # 変換
    elif menu == "3":
        kouho, gobi = skk.to_kouho(token)
        if kouho != None:
            print("候補 [ ",end="")
            for i in range(len(kouho)):
                print(str(i+1)+":"+kouho[i]+" ", end="")
            if gobi == None:
                print("]")
            else:
                print("]　" + gobi)
        else:
            print("該当なし", token)
                    
    elif menu == "4":
        pass
