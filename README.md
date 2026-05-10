# rakuten2freee_converter
楽天証券の有価証券取引報告書をfreee会計で読み込めるようにするものです。

# 使い方

1．次を、実行する。

python rakuten_to_free.py

2. 次が現れたら、読み込む楽天証券さんのCSVファイルの名前(とパス)を入力する。

input_file >>

3. 次に、freee会計用に出力するCSVファイルの名前(とパス)を入力する。

4. プレビューがコマンドライン上に出る。

5. 3のファイルが出力される。

# 入出力例

PS C:\Users\ユーザー名> rakuten_to_freee-2.py

input_file >>
c:\Users\ユーザー名\20260509_torihou.csv
input_file isc:\Users\ユーザー名\20260509_torihou.csv

output_file >>
out_converted.csv
ouput_file isout_converted.csv

読み込み中: c:\Users\ユーザー名\20260509_torihou.csv
変換対象: 1件の取引
出力完了: out_converted.csv

プレビュー:
日付,借方科目,借方金額,貸方科目,貸方金額,摘要
2026/01/27,有価証券,1811000,普通預金,1811000,キオクシアホールディングス 100株買付
