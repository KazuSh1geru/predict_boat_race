# 開始日と終了日を指定(YYYY-MM-DD)
START_DATE = "2020-06-01"
END_DATE = "2020-06-07"

# ファイルの保存先を指定　※コラボでGoogleドライブをマウントした状態を想定
SAVE_DIR = "./input/schedule/timetable_lzh/"

# リクエスト間隔を指定(秒)　※サーバに負荷をかけないよう3秒以上を推奨
INTERVAL = 3

# URLの固定部分を指定
FIXED_URL = "http://www1.mbrace.or.jp/od2/B/"

# 日付を扱う datetime モジュールから datetime と timedelta をインポート
from datetime import datetime as dt
from datetime import timedelta as td

# HTTP通信ライブラリの requests モジュールから get をインポート
from requests import get

# OSの機能を利用する os モジュールから makedirs をインポート
from os import makedirs

# 時間を制御する time モジュールから sleep をインポート
from time import sleep

# 開始合図
print("作業を開始します")

# ファイルを保存するフォルダを作成
makedirs(SAVE_DIR, exist_ok=True)

# 開始日と終了日を日付型に変換して格納
start_date = dt.strptime(START_DATE, '%Y-%m-%d')
end_date = dt.strptime(END_DATE, '%Y-%m-%d')

# 日付の差から期間を計算
days_num = (end_date - start_date).days + 1

# 日付リストを格納する変数を定義
date_list = []

# 期間から日付を順に取り出す
for d in range(days_num):
    # 開始日からの日付に変換
    target_date = start_date + td(days=d)

    # 日付(型)を文字列に変換してリストに格納(YYYYMMDD)
    date_list.append(target_date.strftime("%Y%m%d"))

# 日付リストから日付を順に取り出す
for date in date_list:

    # URL用に日付の文字列を生成
    yyyymm = date[0:4] + date[4:6]
    yymmdd = date[2:4] + date[4:6] + date[6:8]

    # URLとファイル名を生成
    variable_url = FIXED_URL + yyyymm + "/b" + yymmdd + ".lzh"
    file_name = "b" + yymmdd + ".lzh"

    # 生成したURLでファイルをダウンロード
    r = get(variable_url)

    # 成功した場合
    if r.status_code == 200:
        # ファイル名を指定して保存
        f = open(SAVE_DIR + file_name, 'wb')
        f.write(r.content)
        f.close()
        print(variable_url + " をダウンロードしました")

    # 失敗した場合
    else:
        print(variable_url + " のダウンロードに失敗しました")

    # 指定した間隔をあける
    sleep(INTERVAL)

# 終了合図
print("作業を終了しました")