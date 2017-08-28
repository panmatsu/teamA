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
   markrt integer not null,
    markrb integer not null,
    marklt integer not null,
    marklb integer not null,
    silhouette text not null
);
"""
con.execute(sql2)

con.close()
