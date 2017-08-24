# -*- coding: utf-8 -*-

import sqlite3
import sys

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db")

sql = u"""
create table keyset (
    id integer,
    name varchar,
    mark varchar,
    silhouette varchar
);
"""
con.execute(sql)
