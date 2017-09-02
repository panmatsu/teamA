###################
#main
##################
import cv2 
import numpy as np 
import os
import time
import sys

import MarkerDetection 
import MarkerJudgement 
import Key 
import PersonAuthentication
import TimeCount
import PoseDetection

if len(sys.argv) == 1:
    cam = cv2.VideoCapture(0)
    ret, back = cam.read()
    if ret == False:
        print('cannot read cam')
        exit(0)
    else:
        #背景画像取得
        back = cv2.cvtColor(back, cv2.COLOR_RGB2GRAY)
if len(sys.argv) == 2:
    cam = cv2.VideoCapture(sys.argv[1])
    #背景画像取得 
    back = cv2.imread('back.png',0)
    
#ログテキスト 
log = open("log.txt","w")

#インスタンス化
md = MarkerDetection.MarkerDetection()
mj = MarkerJudgement.MarkerJudgement()
pd = PersonAuthentication.PersonAuthentication()

#TimeCount(1,2)
#1:何秒間そのポーズを保つか
#2:↑の間に何フレームそのポーズをとっているか
tc = TimeCount.TimeCount(3.0,10)

#PoseDetection(1,2,3,4)
#1:２値化パラメータ
#2:#平滑化パラメータ
#3:ポーズ判定ピクセル数 
#4:フレーム取得回数
sb = PoseDetection.PoseDetection(50,5,15000,10)

#######--dbから鍵参照--#######
key = Key.Key()
while(1):
    ret,db_pose,name = key.getKey(mj)
    if ret == True:
        break

#鍵画像を取得
pose_key = cv2.imread(db_pose,0)

print("Are you "+name+"?")
log.write("get db's data\n")

#フェーズ移行フラッグ
person_flag = False
marker_flag = False

#ポーズ認証を３回ミスしたら終了
count = 0

while(1):
    ret,frame = cam.read()
    if ret == False:
        break
    cp_frame = frame.copy()

    if person_flag == False:
        person_flag = tc.personKeep(pd,cp_frame,log)

    if person_flag == True:
        marker_flag = tc.markerKeep(mj,md,cp_frame,log)
    
    if marker_flag == True:
        j = sb.judge_pose(frame,back,pose_key,log)
        if j == 1:
            print('open you are '+name)
            break
        elif j == 2:
            marker_flag = False
            count += 1
            print('close')
        elif count >= 3:
            print('close you are not '+name)
            break
            
    cv2.imshow('result',frame)
    k = cv2.waitKey(30)
    if k == ord('q'):
        break
log.close()
cv2.destroyAllWindows()
cam.release()

    
