import sys
import os

#ローマ字をカナに変換するための関数を提供するクラス
class Romaji:
    tree = {
        "a":  "あ", "i": "い", "u": "う", "e": "え", "o": "お",
        "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
        "kya": "きゃ", "kyi": "きぃ", "kyu": "きゅ", "kye": "きぇ", "kyo": "きょ",
        "kwa": "くゎ", "kwi": "くぃ", "kwu": "くぅ", "kwe": "くぇ","kwo": "くぉ",
        "sa": "さ", "si": "し", "su": "す", "se": "せ", "so": "そ",
        "sya": "しゃ", "syi": "し", "syu": "しゅ", "sye": "しぇ", "syo": "しょ",
        "sha": "しゃ", "shi": "し", "shu": "しゅ", "she": "しぇ", "sho": "しょ",
        "swa": "すゎ", "swi": "すぃ", "swu": "すぅ", "swe": "すぇ", "swo": "すぉ",
        "ta": "た", "ti": "ち", "tu": "つ", "te": "て", "to": "と",
        "tya": "ちゃ", "tyi": "ちぃ", "tyu": "ちゅ", "tye": "ちぇ", "tyo": "ちょ",
        "tha": "てゃ", "thi": "てぃ", "thu": "てゅ", "the": "てぇ", "tho": "てょ",
        "tsa": "つぁ", "tsi": "つぃ", "tsu": "つ", "tse": "つぇ", "tso": "つぉ",
        "ca": "か", "ci": "し", "cu": "く", "ce": "せ", "co": "こ",
        "cha": "ちゃ", "chi": "ち", "chu": "ちゅ", "che": "ちぇ", "cho": "ちょ",
        "cya": "ちゃ", "cyi": "ちぃ", "cyu": "ちゅ", "cye": "ちぇ", "cyo": "ちょ",
        "qa": "くぁ", "qi": "くぃ", "qu": "く", "qe": "くぇ", "qo": "くぉ",
        "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
        "nya": "にゃ", "nyi": "にぃ", "nyu": "にゅ", "nye": "にぇ", "nyo": "にょ",
        "nwa": "ぬゎ", "nwi": "ぬぃ", "nwu": "ぬぅ", "nwe": "ぬぇ", "nwo": "ぬぉ",
        "ha": "は", "hi": "ひ", "hu": "ふ", "he": "へ", "ho": "ほ",
        "hya": "ひゃ", "hyi": "ひぃ", "hyu": "ひゅ", "hye": "ひぇ", "hyo": "ひょ",
        "fa": "ふぁ", "fi": "ふぃ", "fu": "ふ", "fe": "ふぇ", "fo": "ふぉ",
        "fya": "ふゃ", "fyi": "ふぃ", "fyu": "ふゅ", "fye": "ふぇ", "fyo": "ふょ",
        "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
        "mya": "みゃ", "myi": "みぃ", "myu": "みゅ", "mye": "みぇ", "myo": "みょ",
        "ya": "や", "yi": "い", "yu": "ゆ", "ye": "いぇ", "yo": "よ",
        "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
        "rya": "りゃ", "ryi": "りぃ", "ryu": "りゅ", "rye": "りぇ", "ryo": "りょ",
        "wa": "わ", "wi": "うぃ", "wu": "う", "we": "うぇ", "wo": "うぉ",
        "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
        "gya": "ぎゃ", "gyi": "ぎぃ", "gyu": "ぎゅ", "gye": "ぎぇ", "gyo": "ぎょ",
        "za": "ざ", "zi": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
        "zya": "じゃ", "zyi": "じぃ", "zyu": "じゅ", "zye": "じぇ", "zyo": "じょ",
        "ja": "じゃ", "ji": "じ", "ju": "じゅ", "je": "じぇ", "jo": "じょ",
        "jya": "じゃ", "jyi": "じぃ", "jyu": "じゅ", "jye": "じぇ", "jyo": "じょ",
        "da": "だ", "di": "ぢ", "du": "づ", "de": "で", "do": "ど",
        "dha": "でゃ", "dhi": "でぃ", "dhu": "でゅ", "dhe": "でぇ", "dho": "でょ",
        "dya": "ぢゃ", "dyi": "ぢぃ", "dyu": "ぢゅ", "dye": "ぢぇ", "dyo": "ぢょ",
        "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",
        "bya": "びゃ", "byi": "びぃ", "byu": "びゅ", "bye": "びぇ", "byo": "びょ",
        "va": "ゔぁ", "vi": "ゔぃ", "vu": "ゔ", "ve": "ゔぇ", "vo": "ゔぉ",
        "vya": "ゔゃ", "vyi": "ゔぃ", "vyu": "ゔゅ", "vye": "ゔぇ", "vyo": "ゔょ",
        "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",
        "pya": "ぴゃ", "pyi": "ぴぃ", "pyu": "ぴゅ", "pye": "ぴぇ", "pyo": "ぴょ",
        "xa": "ぁ", "xi": "ぃ", "xu": "ぅ", "xe": "ぇ", "xo": "ぉ",
        "xya": "ゃ", "xyi": "ぃ", "xyu": "ゅ", "xye": "ぇ", "xyo": "ょ",
        "la": "ぁ", "li": "ぃ", "lu": "ぅ", "le": "ぇ", "lo": "ぉ",
        "lya": "ゃ", "lyi": "ぃ", "lyu": "ゅ", "lye": "ぇ", "lyo": "ょ",
        "ltu": "っ", "xtu": "っ", "ltsu": "っ", "xtsu": "っ"
    }
    
    max_unit_len = max([len(k) for k in tree])
  
    #カナ１モウラに変換できるローマ字の並びかどうかを判定する
    @classmethod
    def isUnit(cls, tokens, s=0):
        for i in range(cls.max_unit_len,0,-1):
            if tokens[s:s+i] in cls.tree:
                return True
        return False
  
    @classmethod
    def getUnit(cls, tokens, s=0):
        for i in range(cls.max_unit_len,0,-1):
            if tokens[s:s+i] in cls.tree:
                return cls.tree[tokens[s:s+i]], s+i
        return "",s

    #"ン"に変換すべきかどうかを判定する
    @classmethod
    def isHatsuon(cls, tokens, s=0):
        if s >= len(tokens):
            return False
        if tokens[s] not in ["n","m"]:
            return False
        return True
  
    @classmethod
    def getHatsuon(cls, tokens, s=0):
        return "ん", s+1

    #"ッ"に変換すべきかどうかを判定する
    @classmethod
    def isSokuon(cls, tokens, s=0):
        if s+1 >= len(tokens):
            return False
        if tokens[s] != tokens[s+1]:
            return False
        if not tokens[s].isalpha():
            return False
        return True

    @classmethod
    def getSokuon(cls, tokens, s=0):
        return "っ", s+1

  
    #ローマ字全体をカナに変換する
    @classmethod
    def getKana(cls, tokens, s=0):
        if s >= len(tokens) or s < 0:
            return ""
        kana = ""
        idx = s
        if cls.isUnit(tokens, idx):
            kana, idx = cls.getUnit(tokens, idx)
        elif cls.isHatsuon(tokens, idx):
            kana, idx = cls.getHatsuon(tokens, idx)
        elif cls.isSokuon(tokens, idx):
            kana, idx = cls.getSokuon(tokens, idx)
        else:
            kana, idx = tokens[idx], idx+1
        if idx >= len(tokens):
            return kana
        else:
            return kana + cls.getKana(tokens, idx)     
 
    #大文字、または小文字のアルファベットの並びをカナに変換する  
    @classmethod
    def toKana(cls, text): 
        text = text.lower()
        return cls.getKana(text,0)


if __name__=="__main__":
    testcase = [
        "Hello",
        "I'm",
        "konnichiwa",
        "砂糖",
        "hecchara",
        "ampamman"
    ]
    for t in testcase:
        print(t,Romaji.toKana(t))
