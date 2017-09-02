
import cv2 
import numpy as np 
import os
import time
import sys
import sqlite3
import re
from judge_marker import *
from detect_red_circle import *
from pose_detection import *

if len(sys.argv) == 1:
    cam = cam = cv2.VideoCapture(1)
    ret, back = cam.read()
    if ret == False:
        print('cannot read cam')
        exit(0)
    else:
        back = cv2.cvtColor(back, cv2.COLOR_RGB2GRAY)
if len(sys.argv) == 2:
    cam = cv2.VideoCapture(sys.argv[1])
    #背景画像
    back = cv2.imread('back.png',0)

#ログテキスト
log = open("log.txt","w")

#dbから鍵参照
while(1):
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
        name = row1[1]
        left_ltx = row1[2]
        left_lty = row1[3]
        left_rbx = row1[4]
        left_rby = row1[5]
        right_ltx = row1[6]
        right_lty = row1[7]
        right_rbx = row1[8]
        right_rby = row1[9]
        db_pose = row1[10]

    con.close()
    if idnum == "nodata":
        print("something wrong.")
    else:
        break

print('Are you '+name+'?')
log.write("get db's data\n")
#鍵
key_pose = cv2.imread(db_pose,0)
set_lock_position(left_ltx,left_lty,left_rbx,left_rby,right_ltx,right_lty,right_rbx,right_rby)

#特徴量計算(体)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#分類器のパラメータ
hogParams = {'winStride':(8,8),'padding':(32,32),'scale':1.05}

#秒数判定の最低フレーム数
f = 10

face_color = (255,0,0)
body_color = (0,255,0)

#顔判別の分類器データのパス
cascade_path = "haarcascade_frontalface_alt.xml"
#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

human_flag = False
marker_flag = False
marker_key = False
getFrame_flag = False

poseWhitePix = 0

frame_count = 0

time_start = 0.0
marker_time_start = 0.0

human_frame_per_3sec = 0
marker_frame_per_3sec = 0

count = 0
while(1):
    ret, frame = cam.read()
    if ret == False:
        break
    
    proFrame = frame.copy()

    #人物認識実行
    if marker_flag == False:
        human,r = hog.detectMultiScale(proFrame,**hogParams)
        face = cascade.detectMultiScale(proFrame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        
        if len(human) != 0:
            for(x,y,w,h) in human:
                cv2.rectangle(proFrame,(x,y),(x+w,y+h),body_color,3)
            #print('身体認識')
            log.write("detect dody\n")
        if len(face) != 0:
            for rect in face:
                cv2.rectangle(proFrame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), face_color, thickness=2)
            #print('顔認識')
            log.write("detect face\n")
           
        if len(human) != 0 and len(face) != 0:
            human_flag = True
            #print('detect human')
            log.write("detect human\n")
        else:
            human_flag = False
            #print('cannot detect human')
            log.write("cannot detect human\n")

    #human_flag==Trueが3sec続く
    #    marker_flag = True
    if human_flag == True and time_start==0.0 and marker_flag == False:
        time_start = time.time()
        #print('start time measurement(person)')
        log.write("start time measurement(marker)\n")
    if time_start != 0 and human_flag == True:
        human_frame_per_3sec = human_frame_per_3sec + 1
    if time_start != 0 and time.time() - time_start > 3.0 and human_frame_per_3sec > f:
        marker_flag = True
        time_start = 0
        human_frame_per_3sec = 0
        print('you are person')
        log.write("open person key\n")
    if time_start != 0 and time.time() - time_start > 3.0 and human_frame_per_3sec < f:
        marker_flag = False
        time_start = 0
        human_frame_per_3sec = 0
        print('you are not person')
        log.write("close person key\n")


    if marker_flag == True:
        #マーカー認証
        #範囲内にいる->marker_key = True
        if(detect_red_circle(frame,log)==True):
                if judge_marker(frame,log) == True:
                    marker_key = True
                    #print('黄円範囲内')
                    log.write("marker is in key area\n")
                else:
                    marker_key = False
                    #print('黄円範囲外')
                    log.write("marker is not in key area\n")
      
        #marker_key==Trueが3sec続く
        #   getFrame_flag = True
        if marker_key == True and marker_time_start == 0 and marker_key == True:
            marker_time_start = time.time()
            #print('start time measurement(marker)')
            log.write("start time measurement(marker)\n")
        if marker_time_start != 0 and marker_key == True:
            marker_frame_per_3sec = marker_frame_per_3sec + 1
        if marker_time_start != 0 and time.time() - marker_time_start > 3.0 and marker_frame_per_3sec > f:
            getFrame_flag = True
            marker_time_start = 0.0
            maker_frame_per_3sec = 0
            print('marker key open')
            log.write("marker key open\n")
        if marker_time_start != 0 and time.time() - marker_time_start > 3.0 and marker_frame_per_3sec:
            getFrame_flag = False
            marker_time_start = 0.0
            maker_frame_per_3sec = 0
            print('marker key close')
            log.write("marker key close\n")

    #getFrame_flag==Tureなら１０フレーム取得
    if getFrame_flag == True and frame_count < 10:
        poseWhitePix += cmp_pose(frame,frame_count,back,key_pose,log)
        log.write("get silhouette farme\n")
        frame_count += 1

    if frame_count == 10:
        #フレームリストのシルエット化
        #鍵との比較=>poseWhitePixリストに追加
        #ポーズシルエット開錠の判定
        #リストの平均値取得
        if judge_pose(poseWhitePix,frame_count,log) == True:
            log.write("calc white pix\n")
            pose_key = True
            #開錠処理
            print('pose key open')
            log.write("pose key open\n")
            break
        else:
            pose_key = False
            print('pose key close')
            log.write("pose key close\n")
            marker_key = False
            getFrame_flag = False
            frame_count = 0
            poseWhitePix = 0
            break
        
        
    cv2.imshow('result', frame)
    cv2.imshow('human', proFrame)
    key = cv2.waitKey(30)
    if key == ord('q'):
        log.write("exit (input q button)")
        break
log.close()
cv2.destroyAllWindows()
cam.release()

