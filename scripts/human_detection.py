
import cv2
import numpy as np
import os
import sys

#カメラキャプチャー
cam = cv2.VideoCapture(sys.argv[1])

#特徴量計算
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#分類器のパラメータ
hogParams = {'winStride':(8,8),'padding':(32,32),'scale':1.05}

#データのパス
cascade_path = "haarcascade_frontalface_alt.xml"
#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 


face_color = (255,0,0)
body_color = (0,255,0)

try:
    while(1):
        ret, frame = cam.read()
        if ret == False:
            break
        
        #人物（体）認識の実行
        human,r = hog.detectMultiScale(frame,hitThreshold=-0.5, winStride=(8,8), padding=(0,0), scale=1.05, finalThreshold=5)    
        for(x,y,w,h) in human:
            cv2.rectangle(frame,(x,y),(x+w,y+h),body_color,3) 
    
        #人物（顔）認識の実行
        facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        for rect in facerect:
            cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), face_color, thickness=2)

        cv2.imshow('result', frame)
        key = cv2.waitKey(30)
        if key == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    cam.release()

