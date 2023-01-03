from requests import get
from bs4 import BeautifulSoup

target_url = "https://www.boatrace.jp/owpc/pc/race/odds2tf?rno=1&jcd=21&hd=20210206"

if __name__ == "__main__":
    html = get(target_url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # css selectorで指定したHTMLタグの中身を取得
    odds_tables = soup.find_all("table")
    # 2連単オッズ
    odds_table = odds_tables[2]
    print(odds_table)
    # print(odds_table[1])
    
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
        
    print(csv_text)