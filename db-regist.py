# -*- coding: utf-8 -*-
# python db-regist.py **.csv とcsvファイルの指定

import sqlite3
import sys
import csv

# コマンドラインよりcsvファイル名取得
dat = sys.argv[1]

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db")

# table keyset
# -> id, name, mark, silhouette

# csvを開く
reader = csv.reader(open(dat))
for row in reader:
    sql = "insert into keyset values (" + row[0] + ", \'" + row[1] + "\', \'" + row[2] + "\', \'" + row[3] + "\')"
    con.execute(sql)

# table:keysetの内容一括表示
c = con.cursor()
c.execute("select * from keyset")
for row1 in c:
    print(row1[0], row1[1], row1[2], row1[3])

con.close()
