from requests import get
from bs4 import BeautifulSoup

target_url = "https://www.boatrace.jp/owpc/pc/race/oddstf?rno=1&jcd=21&hd=20210206"

if __name__ == "__main__":
    html = get(target_url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    
    odds_tables = soup.find_all("table")
    
    odds_table = odds_tables[1]
    # print(odds_table)
    
    # tbodyを指定
    odds_table_elements = odds_table.select("tbody")
    # オッズデータを格納する変数を定義
    csv_row = []

    # オッズデータを取得して変数に格納
    for row in odds_table_elements:
        for cell in row.select("td.oddsPoint"):
            csv_row.append(cell.get_text())
    

    # CSVデータを格納する変数を定義
    csv_text = ""

    # オッズデータにコロンを付けて変数に格納
    for odds in csv_row:
        csv_text += "," + odds
        
    print(csv_text)