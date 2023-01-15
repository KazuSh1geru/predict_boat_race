from os.path import dirname, abspath
import sys

# job_exex.pyから2つ上のディレクトリの絶対パスを取得し、sys.pathに登録する
parent_dir = dirname(dirname(abspath(__file__))) # 追加
if parent_dir not in sys.path: # 追加
    sys.path.append(parent_dir) # 追加
    
# レースコードが格納されているCSVファイルを指定　※最初の列に格納されていること
from constants import CLEAN_DATA_FILE_PATH

# オッズデータを格納するCSVファイルの保存先を指定
ODDS_FILE_DIR = "./input/results/odds_csv/"

# 舟券種別を指定
BET_TYPE = "3f"

# オッズデータを格納するCSVファイルの名前を指定
ODDS_FILE_NAME = f"odds_{BET_TYPE}_YYYYMMDD-YYYYMMDD.csv"

# オッズデータを格納するCSVファイルのヘッダーを指定
ODDS_FILE_HEADER = "レースコード,\
3連複_1-2-3,\
3連複_1-2-4,\
3連複_1-2-5,\
3連複_1-2-6,\
3連複_1-3-4,3連複_2-3-4,\
3連複_1-3-5,3連複_2-3-5,\
3連複_1-3-6,3連複_2-3-6,\
3連複_1-4-5,3連複_2-4-5,3連複_3-4-5,\
3連複_1-4-6,3連複_2-4-6,3連複_3-4-6,\
3連複_1-5-6,3連複_2-5-6,3連複_3-5-6,3連複_4-5-6\n"


# URLの固定部分を指定
FIXED_URL = "https://www.boatrace.jp/owpc/pc/race/odds"


# リクエスト間隔を指定(秒)　※サーバに負荷をかけないよう3秒以上を推奨
INTERVAL = 3

# HTMLからデータを取り出すモジュール BeautifulSoup をインポート
from bs4 import BeautifulSoup

# HTTP通信ライブラリの requests モジュールから get をインポート
from requests import get

# 時間を制御する time モジュールから sleep をインポート
from time import sleep

# OSの機能を利用するパッケージ os をインポート
import os

# CSVファイルの読み書きを行う csv モジュールをインポート
import csv

# datetimeを扱う
from dateutil import parser
from datetime import datetime

# Webサイトからオッズデータを抽出する関数 get_odds を定義
def get_odds(target_url):
    # BeautifulSoupにWebサイトのコンテンツを渡す
    html = get(target_url)
    soup = BeautifulSoup(html.content, 'html.parser')

    # Webサイトからコピーしたcss selectorを貼り付け　※3連複と2連単は同じ
    odds_tables = soup.find_all("table")
    

    # オッズデータがあった場合
    try:
        # 3連単オッズ は 2つ目
        odds_table = odds_tables[1]
        # tbodyを指定
        odds_table_elements = odds_table.select_one("tbody")

        # trを指定しリストとして格納
        row_list = odds_table_elements.select("tr")

        # オッズデータを格納する変数を定義
        csv_row = []

        # オッズデータを取得して変数に格納
        for row in row_list:
            for cell in row.select("td.oddsPoint"):
                csv_row.append(cell.get_text())

        # CSVデータを格納する変数を定義
        csv_text = ""

        # オッズデータにコロンを付けて変数に格納
        for odds in csv_row:
            csv_text += "," + odds


    # オッズデータがなかった場合
    except:
        csv_text = "," + "No data"

    return csv_text


# 開始合図
print("作業を開始します")

# オッズデータを格納するCSVファイルを保存するフォルダを作成
os.makedirs(ODDS_FILE_DIR, exist_ok=True)

# オッズデータを格納するCSVファイルを作成しヘッダ情報を書き込む
with open(ODDS_FILE_DIR + ODDS_FILE_NAME, "w", encoding="shift_jis") as csv_file:
    csv_file.write(ODDS_FILE_HEADER)

    # 先頭にwithを記載しているのでclose( )関数の処理は不要
    # csv_file.close()

# レースコードを取得してURLを生成しオッズデータを取得
with open(CLEAN_DATA_FILE_PATH, "r", encoding="shift_jis") as race_code_file:
    reader = csv.reader(race_code_file)

    # ヘッダー行をスキップ
    header = next(reader)

    # レースコードを取得するCSVファイルを1行ずつ読み込む
    for row in reader:
        # 最初の列(レースコード)を格納
        race_code = row[0]
        
        # 2017年以降しかオッズデータを確認できなかった
        race_year = parser.parse(race_code[0:4])
        target_year = datetime.strptime("20170101", "%Y%m%d")
        # ターゲットでなかったらスキップ
        if race_year < target_year:
            continue

        # 3レターコードと場コードの対応表
        dict_stadium = {'KRY': '01', 'TDA': '02', 'EDG': '03', 'HWJ': '04',
                        'TMG': '05', 'HMN': '06', 'GMG': '07', 'TKN': '08',
                        'TSU': '09', 'MKN': '10', 'BWK': '11', 'SME': '12',
                        'AMG': '13', 'NRT': '14', 'MRG': '15', 'KJM': '16',
                        'MYJ': '17', 'TKY': '18', 'SMS': '19', 'WKM': '20',
                        'ASY': '21', 'FKO': '22', 'KRT': '23', 'OMR': '24'
                        }

        # レースコードからレース回・レース場(場コード)・レース日を取得
        race_round = race_code[11:13]
        stadium_code = dict_stadium[race_code[8:11]]
        date = race_code[0:8]

        # URLを生成
        target_url = FIXED_URL + BET_TYPE + "?rno=" + race_round \
                     + "&jcd=" + stadium_code + "&hd=" + date

        print(target_url + " からオッズデータを取得します")

        # 関数 get_odds にURLを渡しオッズデータを取得する
        odds_data = get_odds(target_url)

        # CSVファイルを追記モードで開き、レースコードとオッズデータを書き込む
        with open(ODDS_FILE_DIR + ODDS_FILE_NAME, "a", encoding="shift_jis") as csv_file:
            csv_file.write(row[0] + odds_data + "\n")

        # 指定した間隔をあける
        sleep(INTERVAL)

# 終了合図
print("作業を終了しました")