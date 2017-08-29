# -*- coding: utf-8 -*-

import sqlite3


# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db")

# dbkey.db内にkeyset tableが存在するか否か
cur = con.cursor()
cur.execute("select count(*) from sqlite_master where type='table' and name='keyset'")
for catalog in cur.fetchall():
    tableName = catalog[0]

# 存在する場合tableをdrop
if tableName == 1:
    sql = "drop table keyset;"
    con.execute(sql)

# table keysetの作成
sql2 = u"""
create table keyset (
    id integer unique not null,
    name text not null,
    left_ltx integer not null,
    left_lty integer not null,
    left_rbx integer not null,
    left_rby integer not null,
    right_ltx integer not null,
    right_lty integer not null,
    right_rbx integer not null,
    right_rby integer not null,
    pose text not null
);
"""
con.execute(sql2)

con.close()
