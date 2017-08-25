# -*- coding: utf-8 -*-

import sqlite3


# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db")

sql = "drop table keyset;"
con.execute(sql)

sql2 = u"""
create table keyset (
    id integer unique not null,
    name varchar not null,
    mark varchar not null,
    silhouette varchar not null
);
"""
con.execute(sql2)

con.close()
