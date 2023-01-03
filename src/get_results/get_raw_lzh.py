# 開始日と終了日を指定(YYYY-MM-DD)
START_DATE = "2005-01-01"
END_DATE = "2020-12-31"

# ファイルの保存先を指定　※コラボでGoogleドライブをマウントした状態を想定
SAVE_DIR = "./input/raw_lzh/"

# リクエスト間隔を指定(秒)　※サーバに負荷をかけないよう3秒以上を推奨
INTERVAL = 3

# URLの固定部分を指定
FIXED_URL = "http://www1.mbrace.or.jp/od2/K/"

from time import sleep
from requests import get

# 日付を扱うための datetime モジュールをインポート
from datetime import datetime as dt
from datetime import timedelta as td

# フォルダ(ディレクトリ)を作成する makedirs モジュールをインポート
from os import makedirs

# 開始合図
print("作業を開始します")

# ファイルを格納するフォルダを作成
makedirs(SAVE_DIR, exist_ok=True)

# 開始日と終了日を日付型に変換して格納
start_date = dt.strptime(START_DATE, '%Y-%m-%d')
end_date = dt.strptime(END_DATE, '%Y-%m-%d')

# 日付の差から期間を計算
days_num = (end_date - start_date).days + 1

# 日付リストを格納する変数
date_list = []

# 日付リストを生成
for i in range(days_num):
    # 開始日から日付を順に取得
    target_date = start_date + td(days=i)

    # 日付型を文字列に変換してリストに格納(YYYYMMDD)
    date_list.append(target_date.strftime("%Y%m%d"))

# URL生成とダウンロード
for date in date_list:

    # URL生成
    yyyymm = date[0:4] + date[4:6]
    yymmdd = date[2:4] + date[4:6] + date[6:8]

    variable_url = FIXED_URL + yyyymm + "/k" + yymmdd + ".lzh"
    file_name = "k" + yymmdd + ".lzh"

    # ダウンロード
    r = get(variable_url)

    # 成功した場合
    if r.status_code == 200:
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