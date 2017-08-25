# -*- codeing: utf-8 -*-
# python db-regist.py **.csv とcsvファイルの指定

import sqlite3
import sys
import csv

# コマンドラインよりcsvファイル名取得
dat = sys.argv[1]

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db", isolation_level=None)

# table keyset
# -> id, name, mark, silhouette

# csvを開く
reader = csv.reader(open(dat))
for row in reader:
    sql = "insert into keyset values (" + row[0] + ", \'" + row[1] + "\', \'" + row[2] + "\', \'" + row[3] + "\')"
    con.execute(sql)

con.close()
