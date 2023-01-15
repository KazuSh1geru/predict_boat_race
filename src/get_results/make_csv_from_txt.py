# テキストファイルが保存されている場所を指定
TEXT_FILE_DIR = "./input/results/txt/"

# CSVファイルを保存する場所を指定
CSV_FILE_DIR = "./input/results/csv_racecode/"

# CSVファイルの名前を指定　※YYYYMMDDには対象期間を入力
CSV_FILE_NAME = "results_YYYYMMDD-YYYYMMDD.csv"

# CSVファイルのヘッダーを指定
CSV_FILE_HEADER = "レースコード,タイトル,日次,レース日,レース場,レース回,\
3連単_組番,3連単_払戻金,3連複_組番,3連複_払戻金,2連単_組番,2連単_払戻金,2連複_組番,2連複_払戻金\n"

# OSの機能を利用するパッケージ os をインポート
import os

# 正規表現をサポートするモジュール re をインポート
import re


# テキストファイルからデータを抽出し、CSVファイルに書き込む関数 get_data を定義
def get_data(text_file):
    # CSVファイルを追記モードで開く
    csv_file = open(CSV_FILE_DIR + CSV_FILE_NAME, "a", encoding="shift_jis")

    # テキストファイルから中身を順に取り出す
    for contents in text_file:
        exit_loop = False
        # キーワード「競争成績」を見つけたら(rは正規表現でraw文字列を指定するおまじない)
        if re.search(r"競走成績", contents):
            # 1行スキップ
            text_file.readline()

            # タイトルを格納
            line = text_file.readline()
            title = line[:-1].strip()

            # 1行スキップ
            text_file.readline()

            # 日次・レース日・レース場を格納
            line = text_file.readline()
            day = line[3:7].replace(' ', '')
            date = line[17:27].replace(' ', '0')
            stadium = line[62:65].replace('　', '')
            # たまにうまくいかない
            if stadium == "場\n":
                stadium = line[-8:-5].replace('　', '')


        # キーワード「払戻金」を見つけたら
        if re.search(r"払戻金", contents):

            # レース結果を読み込む行(開始行)を格納
            line = text_file.readline()

            # 空行まで処理を繰り返す = 1〜12レースまでの結果を取得
            while line != "\n":
                # レース結果を格納
                results = line[10:13].replace(' ', '0') + "," \
                          + line[15:20] + "," + line[21:28].strip() + "," \
                          + line[32:37] + "," + line[38:45].strip() + "," \
                          + line[49:52] + "," + line[53:60].strip() + "," \
                          + line[64:67] + "," + line[68:75].strip()

                # レースコードを生成
                dict_stadium = {'桐生': 'KRY', '戸田': 'TDA', '江戸川': 'EDG', '平和島': 'HWJ','びわこ': 'BWK',
                                '多摩川': 'TMG', '浜名湖': 'HMN', '蒲郡': 'GMG', '常滑': 'TKN',
                                '津': 'TSU', '三国': 'MKN', '琵琶湖': 'BWK', '住之江': 'SME',
                                '尼崎': 'AMG', '鳴門': 'NRT', '丸亀': 'MRG', '児島': 'KJM',
                                '宮島': 'MYJ', '徳山': 'TKY', '下関': 'SMS', '若松': 'WKM',
                                '芦屋': 'ASY', '福岡': 'FKO', '唐津': 'KRT', '大村': 'OMR'
                                }

                race_round = line[10:12].replace(' ','0')
                race_code = date[0:4] + date[5:7] + date[8:10] + dict_stadium[stadium] + race_round[0:2]

                # 抽出したデータをCSVファイルに書き込む
                csv_file.write(race_code + "," + title + "," + day + "," + date + "," + stadium + "," + results + "\n")

                # 次の行を読み込む
                line = text_file.readline()

    # CSVファイルを閉じる
    csv_file.close()


# 開始合図
print("作業を開始します")

# CSVファイルを格納するフォルダを作成
os.makedirs(CSV_FILE_DIR, exist_ok=True)

# CSVファイルを作成しヘッダ情報を書き込む
csv_file = open(CSV_FILE_DIR + CSV_FILE_NAME, "w", encoding="shift_jis")
csv_file.write(CSV_FILE_HEADER)
csv_file.close()

# テキストファイルのリストを取得
text_file_list = os.listdir(TEXT_FILE_DIR)

# リストからファイル名を順に取り出す
for text_file_name in text_file_list:

    # 拡張子が TXT のファイルに対してのみ実行
    if re.search(".TXT", text_file_name):
        # テキストファイルを開く
        text_file = open(TEXT_FILE_DIR + text_file_name, "r", encoding="shift_jis")
        # 関数 get_data にファイル(オブジェクト)を渡す
        get_data(text_file)

        # テキストファイルを閉じる
        text_file.close()

print(CSV_FILE_DIR + CSV_FILE_NAME + " を作成しました")

# 終了合図
print("作業を終了しました")