
import cv2 
import numpy as np 
import os
import time
from judge_marker import *
from marker_detection import *
from matplotlib import pyplot as pyplot

#カメラキャプチャー
cam = cv2.VideoCapture(0)

#背景画像
back = cv2.imread('back.png')

#現時点では鍵の探索は未実装
#鍵
key_pose = cv2.imread('pose.png')
marker = cv2.imread('template.png',


#特徴量計算(体)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#分類器のパラメータ
hogParams = {'winStride':(8,8),'padding':(32,32),'scale':1.05}


#２値化のパラメータ
t = 50
# 平滑下のパラメータ
n = 5
#3秒間に何フレームで認証するか
f = 100
#ノイズ消しのパラメータ
kernelo = np.ones((5,5),np.uint8)
#穴埋めパラメータ
kernelc = np.ones((5,5),np.uint8)
#ポーズ判定ピクセル
j = 7000


face_color = (255,0,0)
body_color = (0,255,0)

#顔判別の分類器データのパス
cascade_path = "haarcascade_frontalface_alt.xml"
#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

human_flag = False
marker_key = False
getFrame_flag = False

poseFrameList = []
poseWhitePix = []

frame_count = 0

time_start = None
marker_time_start = None

human_frame_per_3sec = 0
marker_frame_per_3sec = 0
while(1):
    ret, frame = cam.read()
    if ret == False:
        break

    #人物認識実行
    if detect_marker(frame,marker) == False:
        human,r = hog.detectMultiScale(frame,**hogParams)
        face = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        if human == [] and face == []:
            human_flag = False
        else:
            human_flag = True
            for(x,y,w,h) in human:
                cv2.rectangle(frame,(x,y),(x+w,y+h),body_color,3)
            for rect in face:
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), face_color, thickness=2)
    #human_flag==Trueが3sec続く
    #    marker_flag = True
    if human_flag == True and time_start == None and marker_key != False:
        time_start = time.time()
    if time_start != None and human_flag == True:
        human_frame_per_3sec = human_frame_per_3sec + 1
    if time_start != None and time.time() - time_start > 3.0 and human_frame_per_3sec > f:
        marker_flag = True
        time_start = None
        human_frame_per_3sec = 0
    else:
        marker_flag = False
        time_start = None
        human_frame_per_3sec = 0
        


    if marker_flag == True:
        #マーカー認証
        #範囲内にいる->marker_key = True
        if(detect_marker(frame,marker)==True):
            positionList = get_position()
            for i in positionList:
                if judge_maker(positionList) == True:
                    marker_key = True
                else:
                    marker_key = False
      
    #marker_key==Trueが3sec続く
    #   getFrame_flag = True
    if marker_key == True and marker_time_start == None and marker_key != False:
        marker_time_start = time.time()
    if time_start != None and marker_key == True:
        marker_frame_per_3sec = marker_frame_per_3sec + 1
    if marker_time_start != None and time.time() - marker_time_start > 3.0 and marker_frame_per_3sec > f:
        getFrame_flag = True
        marker_time_start = None
        maker_frame_per_3sec = 0
    else:
        getFrame_flag = False
        marker_time_start = None
        maker_frame_per_3sec = 0
        

    #getFrame_flag==Tureなら１０フレーム取得
    if getFrame_flag == True and frame_count < 10:
        poseList.extend(frame)
        frame_count = frame_count + 1
    
  
    if frame_count == 10:
        #フレームリストのシルエット化
        #鍵との比較=>poseWhitePixリストに追加
        for i in poseList:
            fgmask = cv2.absdiff(i,back)
            ret, binal = cv2.threshold(fgmask, t, 255, cv2.THRESH_BINARY)
            binal = cv2.medianBlur(binal, n)
            erosion = cv2.erode(binal,kernel,iterations = 1)
            opening = cv2.morphologyEx(binal, cv2.MORPH_OPEN, kernelo)
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelc)
            result = cv2.absdiff(closing,key_pose)
            poseWhitePix.extend(cv2.countNonZero(result))
        #リストの平均値取得
        poseAve = sum(poseWhitePix)/len(poseWhitePix)
        #ポーズシルエット開錠の判定
        if poseAve < j:
            pose_key = True
        else:
            pose_key = False
        
        if pose_key == True:
            #開錠処理
            print('open')
            break
        else:
            print('close')
            marker_key = False
            getFrame_flag = False
            frame_count = 0
            poseFrameList = []
            poseWhitePix = []
        
        
    cv2.imshow('result', frame)
    key = cv2.waitKey(30)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
cam.release()

