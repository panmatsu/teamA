# -*- codeing: utf-8 -*-
# python db-regist.py **.csv とcsvファイルの指定

import sqlite3
import sys
import csv
import re

# コマンドラインよりcsvファイル名取得
dat = sys.argv[1]
pas = sys.argv[2]

a = re.match(r'\d+', pas)

if a:
    sql = "select * from keyset where id == " + pas
    
else:
    sql = "select * from keyset where name == \"" + pas + "\""

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db")

# table keyset
# -> id, name, mark, silhouette

# csvを開く
reader = csv.reader(open(dat))
for row in reader:
    sql2 = "insert into keyset values (" + row[0] + ", \'" + row[1] + "\', \'" + row[2] + "\', \'" + row[3] + "\')"
    con.execute(sql2)

# table:keysetの内容一括表示
c = con.cursor()
c.execute(sql)
for row1 in c:
    print(row1[0], row1[1], row1[2], row1[3])

con.close()
