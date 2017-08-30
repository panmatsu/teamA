# -*- codeing: utf-8 -*-

import numpy as np
import sqlite3
import sys
import cv2
import shutil
import os
import time

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
        print("please push key｢v｣, and pose for a key!")
    elif key == ord('v'):
        output_filename = str(nid) + "_" + nname + ".avi"
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        four_cc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 30.0
        writer = cv2.VideoWriter(output_filename, four_cc, fps, (frame_width, frame_height))
        # record first frame.
        writer.write(frame)

        while True:
            _, img = cap.read()
            if img is None:
                break
            cv2.imshow('capture', img)
            writer.write(img)
            k = cv2.waitKey(10)
            if k is ord('q'):
                break

        cap.release()
        writer.release()

recap = cv2.videoCapture(output_filename)
ret, poseframe = recap.read()
cnt = 0

while(True):
    if poseframe is None:
        print("FINISH!!")
        break

    gray = cv2.cvtColor(poseframe, cv2.COLOR_BGR2GRAY)
    cv2.imshow('poseframe',gray)
    pkey = cv2.waitkey(1)
    if pkey == ord('q'):
        break
    elif pkey == ord('n'):
        ret, poseframe = recap.read()
    elif key == ord('s'):
        file_name = "gray_pose"
        cv2.imwright(file_name,gray)
        cnt += 1
recap.release()


    #### マーカー範囲指定
    #### 読み込むなりなんなりして取得、仮設定中
left_ltx = 0
left_lty = 0
left_rbx = 0
left_rby = 0
right_ltx = 0
right_lty = 0
right_rbx = 0
right_rby = 0
#### ポーズの画像
#pose = sys.argv[7]
pose = "s1.png"

#        file_name = str(nid) + ".png"
#    print(file_name)
#    cv2.imwrite(file_name, gray)
#    move = "img/" + file_name
#    shutil.move(file_name, move)

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db", isolation_level=None)
sqlleft = str(left_ltx) + ", " + str(left_lty) + ", " + str(left_rbx) + ", " + str(left_rby)
sqlright = str(right_ltx) + ", " + str(right_lty) + ", " + str(right_rbx) + ", " + str(right_rby)
sql = "insert into keyset values (" + str(nid) + ", \'" + nname + "\', " + sqlleft + ", " + sqlright + ", \'" + pose + "\')"
print(sql)
## 実行
#con.execute(sql)
con.close()


