# pico_MicroPython_skk
Raspberry Pi Pico MicroPython用 SKK日本語変換ライブラリpyskk

## 概要

本pyskkライブラリは、Raspberry Pi Pico MicroPython用の日本語変換を補助するライブラリです。  
実装には「かな漢字変換プログラム SKK」の辞書を利用しています。  

Raspberry Pi Pico 用ですが、他の環境でも利用可能です。  
Window 11上のPython 3.10、Raspberry Pi PicoのCircuitPythonでも動作しました。  
SRAMの消費を抑えるため、辞書データはフラッシュメモリ上にファイルとして配置しています。  


※ 本ライブラリの実装にあたり、以下のコンテンツを利用及び流用させて頂いております。 
* SKK dictionary files https://github.com/skk-dev/dict  
  SKK-JISYO.M (ミドルサイズ辞書)  

* PythonModule - ローマ字カタカナ変換   
  https://github.com/JiroShimaya/PythonModule/tree/main/Romaji   
  Romajiモジュールを修正をひらがな変更に修正、  
  変換用テーブルをjsonファイルから読み込みではなく、辞書型テーブルに変更しています。

  * 関連文献：ローマ字をカタカナに変換する【python】  
  https://qiita.com/shimajiroxyz/items/00449918350ea0bb47b9  


## 仕様
* 辞書データ：SKK辞書ファイル SKK-JISYO.M相当 (ミドルサイズ辞書)
* 辞書ファイルサイズ：211Kバイト 
* 収録用語数： 8346ワード
* 収録文字コード：UTF-8

## インストール方法
配布ファイルのlib下のファイルをRaspberry Pi Pico上の/libに配置してください。  
　/lib  
　　├ syskk  
　　└ Romaji 

## 使い方
### pyskkモジュール pyskkクラス

#### ■ インポート方法
【書式】  
`from pyskk import pyskk`  

#### ■ コンストラクタ
【書式】  
`pyskk(path=None)`

【引数】  
`path`: 辞書ファイルのパス

【説明】
日本語変換pyskkクラスのインスタンス生成を行います。  
インスタンス生成時においては、辞書ファイルのパス指定が可能です。  

辞書ファイル ssk_dic_m.binのパスはcpython/pythonでは意識する必要がありません。  
MicroPython、CircuitPython環境では/lib/pyskk/ssk_dic_m.bin がデフォルトのパスとなります。   
デフォルトと異なるディレクトリに配置する場合は、コンストラクタにてパスを指定してください。

#### ■ 日本語変換の利用開始
【書式】  
`begin()`

【引数】  
なし  

【戻り値】  
なし  

【説明】
日本語変換の利用を開始します。  
辞書ファイルの利用を開始（ファールのオープン）します。  
辞書ファイルは利用終了end()を実行するまでオープンしたままの状態となります。  
辞書ファイルが存在しない場合や、読み込みが出来ない場合は例外をスローします。  

#### ■ 日本語変換の利用終了
【書式】  
`end()`

【引数】  
なし  

【戻り値】  
なし  

【説明】
日本語変換の利用を終了します。  
辞書ファイルの閉じます（ファールのクローズ）。  


#### ■ ローマ字ひらがな変換
【書式】  
`to_hiragana(token)`

【引数】  
`token`: 変換対象文字列(ローマ字)  

【戻り値】  
変換した文字列(文字列型)  

【説明】  
tokenで指定したローマ字をひらがなに変換します。  
本関数を使うには、begin()関数による利用開始を行う必要があります。  

【利用例】  
```sample_hiragana.py
from pyskk import pyskk

skk = pyskk.skk()
skk.begin()
print(skk.to_hiragana("konnitiha!"))
skk.end()
```
実行結果：  
こんにちは!  


#### ■ ローマ字カタカナ変換
【書式】  
`to_katakana(token)`

【引数】  
`token`: 変換対象文字列(ローマ字)  

【戻り値】  
変換した文字列(文字列型)  

【説明】  
tokenで指定したローマ字をカタカナに変換します。  
本関数を使うには、begin()関数による利用開始を行う必要があります。  

【利用例】  
```sample_katakana.py
from pyskk import pyskk

skk = pyskk.skk()
skk.begin()
print(skk.to_katakana("konnitiha!"))
skk.end()
```
実行結果：  
コンニチハ!  

#### ■ 変換候補の取得
【書式】  
`to_kouho(token)`

【引数】  
`token`: 変換対象文字列(ローマ字)  

【戻り値】  
変換候補リスト(リスト型)  

【説明】  
tokenで指定したローマ字に対応する変換候補のリストを取得します。  
本関数を使うには、begin()関数による利用開始を行う必要があります。  

読みと送りを考慮して変換する場合、tokenはSKK日本語入力の仕様に基づく記述が必要となります。  
漢字＋送りの形式で変換する場合、漢字と送りの先頭英字を大文字で記述します。  
* MiRu => 見る='見' + 'る'  
* TaBeru => 食べる = '食' + 'べる'
* KaKu => 書く = '書' + 'く'  
* kaku => 各 (送りなし)
* edit => エディット  

変換候補次のようなリスト形式となります。   

1）「送り」ありの場合  
```
>>> skk.to_kouho("KaKu")
(['書', '掛', '欠', '架', '駆', '懸'], 'く')
```
リストの先頭に変換候補のリスト、2番目に送り文字 が格納されます。  

2）「送り」なしの場合  
```
>>> skk.to_kouho("kaku")
(['確', '各', '客', '覚', '革', '隔', '閣', '郭', '較', '赫', '角', '穫', '獲', '殻', '核', '格', '撹', '拡', '廓', '嚇', '劃', '画'], None)
```
リストの先頭に変換候補のリスト、2番目に送り文字にはNoneが格納されます。  

3）変換候補がない場合  
```
>>> skk.to_kouho("hogehoge")
(None, None)
```
リストの先頭、2番目ともNoneが格納されます。  
戻り値のリスト内容で「送りあり」、「送りなし」、「変換候補なし」の判定を適宜行った上、  
適切な処理を行って下さい。  

【利用例】  
```sample_to_kouho.py
>>> from pyskk import pyskk
>>> skk = pyskk.skk()
>>> skk.begin()
>>> skk.to_kouho("MiRu")
(['見', '観', '診'], 'る')
>>> skk.to_kouho("TaBeru")
(['食'], 'べる')
>>> skk.to_kouho("KaKu")
(['書', '掛', '欠', '架', '駆', '懸'], 'く')
>>> skk.to_kouho("kaku")
(['確', '各', '客', '覚', '革', '隔', '閣', '郭', '較', '赫', '角', '穫', '獲', '殻', '核', '格', '撹', '拡', '廓', '嚇', '劃', '画'], None)
>>> skk.end()
>>> 
```

## サンプルプログラム
`test_pyskk.py` はローマ字入力した文字列をひらがな、かたかな、漢字に変換するプログラムです。  
pyskkの主要な機能を使って実装しています。  

実行すると、変換対象のローマ字入力を要求します。  


```
キーワード数: 8346
ローマ字入力(end='@'):
```
入力すると変換する種類を番号で入力します。  
その種類に応じた変換結果を返します。

```
キーワード数: 8346
ローマ字入力(end='@'):TaBeru
[0:無変換 1:ひらがな 2:カタカナ 3:変換 4:取り消し]:3
候補 [ 1:食 ]　べる
ローマ字入力(end='@'):
```

サンプルプログラム `test_pyskk.py` の内容
 
```test_pyskk.py
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
```
