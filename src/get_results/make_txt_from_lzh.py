# ダウンロードしたLZHファイルが保存されている場所を指定
LZH_FILE_DIR = "./input/raw_lzh/"

# 解凍したファイルを保存する場所を指定
TXT_FILE_DIR = "./input/results_txt/"

# 正規表現をサポートするモジュール re をインポート
import re

# LZH形式のファイルを解凍するパッケージ lhafile をインポート
import lhafile

# オペレーティングシステムの機能を利用するパッケージ os をインポート
import os

# 開始合図
print("作業を開始します")

# ファイルを格納するフォルダを作成
os.makedirs(TXT_FILE_DIR, exist_ok=True)

# LZHファイルのリストを取得
lzh_file_list = os.listdir(LZH_FILE_DIR)

# ファイルの数だけ処理を繰り返す
for lzh_file_name in lzh_file_list:

    # 拡張子が lzh のファイルに対してのみ実行
    if re.search(".lzh", lzh_file_name):

        file = lhafile.Lhafile(LZH_FILE_DIR + lzh_file_name)

        # 解凍したファイルの名前を取得
        info = file.infolist()
        name = info[0].filename

        # 解凍したファイルの保存
        open(TXT_FILE_DIR + name, "wb").write(file.read(name))

        print(TXT_FILE_DIR + lzh_file_name + " を解凍しました")

# 終了合図
print("作業を終了しました")