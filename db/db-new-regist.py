# -*- codeing: utf-8 -*-

import sqlite3
import sys
import cv2
import shutil

# コマンドラインより登録データ取得(idと名前)
print("please write your ID >")
rnid = sys.stdin.readline()
nid = rnid.rstrip("\n")
print("please write your name in English >")
rnname = sys.stdin.readline()
nname = rnname.rstrip("\n")

print("please push key｢s｣, we need background picture!")

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    if ret == False:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        file_name = "background.png"
        cv2.imwrite(file_name, gray)
        move = "img/" + file_name
        shutil.move(file_name, move)

        print("please pose for a key!")

##### 3秒人物認証→撮影とか？
#### マーカー範囲指定　rt/rb/lt/lb
#### 読み込むなりなんなりして取得、仮設定中
rt = 0
rb = 0
lt = 0
lb = 0
#### ポーズの画像
#pose = sys.argv[7]
pose = "s1.png"

#        file_name = str(nid) + ".png"
#        print(file_name)
#        cv2.imwrite(file_name, gray)
#        move = "img/" + file_name
#        shutil.move(file_name, move)

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db", isolation_level=None)

sql = "insert into keyset values (" + str(nid) + ", '" + nname + "', " + str(rt) + ", " + str(rb) + ", " + str(lt) + ", " + str(lb) + ", '" + pose + "')"
print(sql)
## 実行
#con.execute(sql)
con.close()
