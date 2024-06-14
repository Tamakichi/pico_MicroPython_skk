#
# pyskk python skk辞書(バイナリファイル)検索
#   指定したキーワードに対応する候補リストを取得する
#   skkバイナリ辞書ファイルのキーワードインデックステーブルを2分探査にて検索する
#   一致したキーワードデータから候補リストを取得する
#

import os
import sys
import struct
from Romaji import Romaji

# 定数
SSK_BINDIC_FILE = "ssk_dic_m.bin"
SSK_BIN_HEAD_SIZE = 12


# skk辞書検索APIクラス
class skk:
    def __init__(self, path=None):
        self.size_keyword = None               # キーワード数
        self.keyword_index_top  = None         # インデックス部先頭アドレス  
        self.keyword_data_top = None           # キーワードデータ先頭アドレス
        self.fp = None                         # 辞書ファイル
        if path == None:
            if sys.implementation.name == 'cpython':
                self.path = os.path.join(os.path.dirname(__file__), SSK_BINDIC_FILE)
            else:
                self.path = "/lib/pyskk/" + SSK_BINDIC_FILE
        else:    
            self.path = path                   # 辞書ファイルパス
 
    # 論理リスト内２分検索
    def binfind(self, key, n, get_at):
        t_p = 0;                  # 検索範囲上限
        e_p = n-1                 # 検索範囲下限
        flg_stop = 0
        d = None
        
        while(True):
            pos = t_p + ((e_p - t_p+1)>>1)
            d = get_at(pos)
            if d == key:      # 等しい
                flg_stop = 1    
                break
            elif key > d:     # 大きい
                t_p = pos + 1   
                if t_p > e_p:
                    break
            else:             # 小さい
                e_p = pos -1
                if e_p < t_p:
                    break
        if not flg_stop:
            return -1
        return pos

    # インデックスファイルの検索
    def find(self, key):
        return self.binfind(key, self.size_keyword, lambda pos:self.get_keyword(pos))

    # 送り指示ありローマ字をキーワードと送りに分ける
    # 例:OkuRu → 'oku', 'ru'
    @staticmethod
    def splitOkuri(token):
        word = ''
        okuri = ''

        # 0文字の場合は、0文字を返す
        if len(token) == 0:
            return word, okuri
        
        # 送りモードの場合、送り文字を調べる
        if token[0].isupper():
            for i in range(1,len(token)):            
                if token[i].isupper():
                    okuri = token[i:]
                    word  = token[0:i]
                    break
            # 送り文字がない場合、送りモードでないとする
            if word == '':
                word = token
                okuei = ''
        else:
            word = token
        return word.lower(), okuri.lower()

    # ヘッダー情報の読み込み
    def load_skk_header(self):
        with open(self.path, mode="rb") as r_f:
            head_data = r_f.read(SSK_BIN_HEAD_SIZE)

        # ヘッダー情報の格納
        self.size_keyword = struct.unpack("<L", head_data[0:4])[0]       # キーワード数
        self.keyword_index_top = struct.unpack("<L", head_data[4:8])[0]  # キーワードインデックス先頭位置
        self.keyword_data_top = struct.unpack("<L", head_data[8:12])[0]  # キーワードデータ先頭位置    
    
    # 辞書サイスの取得
    def len(self):
        return self.size_keyword
    
    
    # 指定キーワードインデックスのキーワードデータの取得
    def get_keywordData(self, index):
        if index >= self.size_keyword:
            return None
        
        self.fp.seek(SSK_BIN_HEAD_SIZE + index*4, 0)
        pos = struct.unpack("<L", self.fp.read(4))[0]
        pos_next = struct.unpack("<L",self.fp.read(4))[0] # ※最終indexの場合の処理は未実装!!
        size = pos_next - pos
        
        self.fp.seek(pos + self.keyword_data_top, 0)
        data_bin = self.fp.read(size)
        keywordData = data_bin.decode('utf-8')
        keyword = keywordData.split(",")
        return keyword[0:-1]


    # 指定キーワードインデックスのキーワードの取得
    def get_keyword(self, index):
        self.fp.seek(SSK_BIN_HEAD_SIZE + index*4, 0)
        pos = struct.unpack("<L",self.fp.read(4))[0]
        self.fp.seek(pos + self.keyword_data_top, 0)    
        keyword_bin = bytearray()
        while (data := self.fp.read(1)) != b',':
            keyword_bin.extend(data)       
        keyword = keyword_bin.decode('utf-8')
        return keyword
 
    # ローマ字=>ひらがな変換
    def to_hiragana(self, token):
        return Romaji.toKana(token)


    # ひらがな=>片仮名変換
    def hiragana_to_katakana(self, token):
        new_token = ""
        for c in token:
            if 0x3041 <= ord(c) <= 0x3093:
                c = chr(ord(c) + 96)
            new_token += c
            
        return new_token

    # 半角=>全角変換
    def to_zenkaku(self, token):
        new_token = ""
        for c in token:
            if 0x21 <= ord(c) <= 0x7e:
                c = chr(ord(c) + 65248)
            elif ord(c) == 0x20:
                c = '　'
            new_token += c
        return new_token

    # ローマ字=>片仮名変換
    def to_katakana(self, token):
        return self.hiragana_to_katakana(self.to_hiragana(token))

    # 日本語辞書変換(送り対応)
    def to_kouho(self, token):
        keyword,okuri = self.splitOkuri(token)
        kana = Romaji.toKana(token)

        # 送り処理
        if okuri != '':
            key = Romaji.toKana(keyword) + okuri[0]
            i = self.find(key)
            if i > 0:
                kouho = self.get_keywordData(i)
                gobi  = Romaji.toKana(okuri)
                return kouho[1:], gobi
            else:
                return None, None
        else:
            key = Romaji.toKana(keyword)
            i = self.find(key)
            if i > 0:
                kouho = self.get_keywordData(i)
                return kouho[1:], None
            else:
                # 候補がない場合、英単語として検索を試みる
                i = self.find(keyword)
                if i > 0:
                    kouho = self.get_keywordData(i)
                    return kouho[1:], None                
                return None, None

    # skk辞書変換利用開始
    def begin(self):
        if self.fp == None:
            self.load_skk_header()
            self.fp = open(self.path, mode="rb")


    # skk ローマ字辞書変換
    def end(self):
        self.fp.close()
        self.fp = None
 