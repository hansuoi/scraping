import requests
from bs4 import BeautifulSoup
import re


# PUBGwikiTOPページにアクセスして、武器ジャンル名を取得する

# TOPページのソースコードを全部ぶっこ抜く
urlName = "https://wikiwiki.jp/pubgjpwiki/"
url = requests.get(urlName)
soup = BeautifulSoup(url.content, "html.parser")


# 5個目のpタグに武器ジャンル名が記載されている

# ソースコードの中からpタグを探し、その中身を配列に格納
para = soup.findAll("p")

# 5個目のpタグに書かれている内容だけぶっこ抜く
weapon_para = para[5]


# 5個目のpタグの中にあるaタグに、各武器ジャンルへのURLが書かれている

# 5個目のpタグの中にあるaタグの中身を配列に格納
weapon = weapon_para.findAll('a')

# weaponの中の、href属性にURLが書いてある
# しかし、URLの冒頭部分'https://wikiwiki.jp'が抜けてるので、その部分を補填する
# 各武器ジャンルへのURLを、urlsに格納する
urls = []
for i in range(len(weapon)):
    urls.append('https://wikiwiki.jp'+weapon[i]['href'])

# 後ろ3つは武器じゃないページなので、切り捨てる
urls = urls[:-3]


# 良さげな情報を集めながらcsvに格納していく
with open('./pubg_data.csv', mode='w', encoding='shift-jis') as f:
    f.write('武器名,威力,射程,反動,連射速度,DPS\n')

    # 各武器ジャンルページのソースコードから、使えそうな情報を保存する
    for urlName in urls:
        # urlsに格納されたページに、順番にアクセス
        url = requests.get(urlName)
        soup = BeautifulSoup(url.content, "html.parser")

        # 各ページから表を探す
        # 1つ目の表は、そのジャンルに該当する武器の一覧。ここからデータを抜く
        table = soup.findAll('table')[0]

        # 表の各行をバラして格納
        guns = table.findAll('tr')
        #print(guns)

        # 0行目は表のタイトルなので無視して、1行目から情報を集めていく
        for i in range(1, len(guns)):
            # tdタグの中に各種情報が格納されている
            gun = guns[i].findAll('td')

            # gunの中身は、
            # [0画像, 1名前, 2威力, 3射程, 4反動, 5連射速度, 6弾薬, 7弾数, 8重さ, 9アタッチメント数]
            # となっており、今回は、
            # [1名前, 2威力, 3射程, 4反動, 5連射速度]
            # だけゲットする。
            # さらに、威力/連射速度をDPSとして、これも格納する

            # stringは、タグに挟まれていた文章だけ抜き出すやつ
            iryoku = gun[2].string
            sokudo = gun[5].string
            if iryoku=='?' or sokudo=='?':
                dps = ''
            else:
                dps = str(float(gun[2].string) * float(gun[5].string))

            data = gun[1].string + ',' + gun[2].string + ',' + gun[3].string + ',' + \
                   gun[4].string + ',' + gun[5].string + ',' + dps + '\n'
            f.write(data)
