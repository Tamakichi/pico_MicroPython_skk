import sys
from pyskk import pyskk

skk = pyskk.skk()
skk.begin()
print("キーワード数:", skk.len())

while True:
    token = input("よみ(end='@'):")
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
        word = skk.romaji_to_hiragana(token)
        print("確定=", word)
        continue
    # カタカナ
    elif menu == "2":        
        word = skk.romaji_to_katakana(token)
        print("確定=", word)
        continue
    # 変換
    elif menu == "3":
        sub_menu = input("[1:通常変換 2:英語変換]:")
        # 通常変換
        if sub_menu == "1":
            kouho, gobi = skk.jp_to_kouho(token)
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
                    
        # ローマ字直接変換
        elif sub_menu == "2":
            kouho = skk.en_to_kouho(token)
            if kouho != None:
                print("候補 [ ",end="")
                for i in range(len(kouho)):
                    print(str(i+1)+":"+kouho[i]+" ", end="")
                print("]")                    
            else:
                print("該当なし:", token)
    elif menu == "4":
        pass


