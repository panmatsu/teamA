# -*- codeing: utf-8 -*-
# python db-regist.py **.csv とcsvファイルの指定

import sqlite3
import sys
import re

def getList():
    # コマンドラインより検索ワード取得
    print("please write your ID or name(English) >")
    rpas = sys.stdin.readline()
    pas = rpas.rstrip("\n")
    idnum = "nodata"

    # 検索ワード1文字目が数字ならTrue
    a = re.match(r'\d+', pas)
    if a:
        sql = "select * from keyset where id == " + pas
    else:
        sql = "select * from keyset where name == \"" + pas + "\""

    # 同フォルダ内のdbkey.dbのDBを展開
    con = sqlite3.connect("dbkey.db", isolation_level=None)

    # table:keysetのhitした内容取得
    c = con.cursor()
    c.execute(sql)
    for row1 in c:
        idnum = row1[0]
    #    name = row1[1]
    #    left_ltx = row1[2]
    #    left_lty = row1[3]
    #    left_rbx = row1[4]
    #   left_rby = row1[5]
    #    right_ltx = row1[6]
    #    right_lty = row1[7]
    #    right_rbx = row1[8]
    #    right_rby = row1[9]
    #    pose = row1[10]
    print(c)
    if idnum == "nodata":
        print("something wrong.")
        return None
    else:
        return c

