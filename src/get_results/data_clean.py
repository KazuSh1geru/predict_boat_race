# OSの機能を利用するパッケージ os をインポート
import os

# CSVファイルの読み書きを行う csv モジュールをインポート
import csv

# CSVファイルのヘッダーを指定
CSV_FILE_HEADER = "レースコード,タイトル,日次,レース日,レース場,レース回,\
3連単_組番,3連単_払戻金,3連複_組番,3連複_払戻金,2連単_組番,2連単_払戻金,2連複_組番,2連複_払戻金\n"

# レースコードが格納されているCSVファイルを指定　※最初の列に格納されていること
RACECODE_FILE_PATH = \
    "./input/results/csv_racecode/results_YYYYMMDD-YYYYMMDD.csv"
CLEAN_DATA_FILE_PATH = \
    "./input/results/csv_racecode/clean_results_YYYYMMDD-YYYYMMDD.csv"


# 開始合図
print("作業を開始します")


# クリーンデータを格納するCSVファイルを作成しヘッダ情報を書き込む
with open(CLEAN_DATA_FILE_PATH, "w", encoding="shift_jis") as csv_file:
    csv_file.write(CSV_FILE_HEADER)

    # 先頭にwithを記載しているのでclose( )関数の処理は不要
    # csv_file.close()

"""
0. '不成立'を検知して削除
1. '中　止'を検知して削除
2. ',,,,,,,' race_codeがない列を削除

"""
with open(RACECODE_FILE_PATH, "r", encoding="shift_jis") as race_code_file:
    reader = csv.reader(race_code_file)

    # ヘッダー行をスキップ
    header = next(reader)

    # レースコードを取得するCSVファイルを1行ずつ読み込む
    for row in reader:
        
        # 0. 中 止の検知と削除
        if any(val.startswith("不成立") for val in row):
            continue
        # 最初の列(レースコード)を格納
        race_code = row[0]
        if race_code == '':
            continue
        # 1. 中 止の検知と削除
        col_3t = row[6]
        if '中　止' in col_3t:
            continue
        
        # CSVファイルを追記モードで書き込む
        with open(CLEAN_DATA_FILE_PATH, "a", encoding="shift_jis") as csv_file:
            csv_file.write(",".join(row) + "\n")

# 終了合図
print("作業を終了しました")