# -*- coding: utf-8 -*-

import sqlite3


# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db")

sql = "drop table keyset;"
con.execute(sql)

sql2 = u"""
create table keyset (
    id integer,
    name varchar,
    mark varchar,
    silhouette varchar
);
"""
con.execute(sql2)

con.close()
