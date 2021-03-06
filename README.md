# SapporoFireActions

札幌市の消防出動情報をスクレイピングする．
http://www.119.city.sapporo.jp/saigai/sghp.html

「過去の災害出動」のテーブル内の昨日の分のデータを取得してJSON形式でファイルに保存する．

## ジオコーディング

住所を経緯度座標に変換する処理は以下のサービスとデータを利用している．

- CSISシンプルジオコーディング実験　(http://newspat.csis.u-tokyo.ac.jp/geocode/modules/geocode/index.php)
- 街区レベル位置参照情報：　国土交通省 国土計画局　(http://nlftp.mlit.go.jp/isj/)

### 実行環境

- Python v3.6.1
- BeautifulSoup 4.5.3

### 実行

python3 ./sapporoFireActionInfo.py

引数でデータを取得する日と出力ファイル形式を選択可能．

```
usage: sapporoFireActionInfo.py [-h] [-o {geojson,json}]
                                [-d {yesterday,today}]

optional arguments:
 -h, --help            show this help message and exit
 -o {geojson,json}, --out {geojson,json}
 -d {yesterday,today}, --day {yesterday,today}
 ```
