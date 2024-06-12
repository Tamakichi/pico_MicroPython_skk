# pico_MicroPython_skk
Raspberry Pi Pico MicroPython用 SKK日本語入力ライブラリ

## 概要

本ライブラリは、Raspberry Pi Pico MicroPython用の日本語入力を補助するライブラリです。  
実装には「かな漢字変換プログラム SKK」の辞書を利用しています。  

Raspberry Pi Pico 用ですが、他の環境でも利用可能です。Window 11上のPython 3.10、CircuitPythonでも動作しました。  
SRAMの消費を抑えるため、辞書データはフラッシュメモリ上にファイルとして配置しています。  

※ 本ライブラリの実装にあたり、以下のコンテンツを利用及び流用させて頂いております。 
* SKK dictionary files https://github.com/skk-dev/dict  
  SKK-JISYO.M (ミドルサイズ辞書)  

* PythonModule の ローマ字カタカナ変換   
  https://github.com/JiroShimaya/PythonModule/tree/main/Romaji  
  * 関連文献：ローマ字をカタカナに変換する【python】  
  https://qiita.com/shimajiroxyz/items/00449918350ea0bb47b9

