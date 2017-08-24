# -*- codeing: utf-8 -*-
# python db-regist.py **.csv とcsvファイルの指定

import sqlite3
import sys
import re

# コマンドラインより検索ワード取得
pas = sys.argv[1]

# 検索ワード1文字目が数字ならTrue
a = re.match(r'\d+', pas)
if a:
    sql = "select * from keyset where id == " + pas
else:
    sql = "select * from keyset where name == \"" + pas + "\""

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db", isolation_level=None)

# table keyset  *db-table-make.py参照
# -> id, name, mark, silhouette

# table:keysetの内容一括表示
c = con.cursor()
c.execute(sql)
for row1 in c:
    print(row1[0], row1[1], row1[2], row1[3])

con.close()
