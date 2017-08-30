import cv2 
import numpy as np 
import os
import time
import sys

cam = cv2.VideoCapture(sys.argv[1])

#背景画像
back = cv2.imread('back.png',0)

#現時点では鍵の探索は未実装
#鍵
key_pose = cv2.imread('pose.png',0)


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
f = 15
#ノイズ消しのパラメータ
kernelo = np.ones((5,5),np.uint8)
#穴埋めパラメータ
kernelc = np.ones((5,5),np.uint8)
#ポーズ判定ピクセル
j = 7000

poseWhitePix = 0
getFrame_flag = False
frame_count = 0

while(1):
    ret, frame = cam.read()
    if ret == False:
        break
    
    if getFrame_flag == True and frame_count < 10:
        print('フレーム取得')
        filename = 'frame' + str(frame_count) + '.png'
        cv2.imwrite(filename,frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        fgmask = cv2.absdiff(gray,back)
        ret, binal = cv2.threshold(fgmask, t, 255, cv2.THRESH_BINARY)
        binal = cv2.medianBlur(binal, n)
        erosion = cv2.erode(binal,kernelo,iterations = 1)
        opening = cv2.morphologyEx(binal, cv2.MORPH_OPEN, kernelo)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelc)
        result = cv2.absdiff(closing,key_pose)
        name = 'diff'+str(frame_count)+'.png'
        cv2.imwrite(name,result)
        poseWhitePix += cv2.countNonZero(result)
        

        frame_count = frame_count + 1
    
  
    if frame_count == 10:
        #フレームリストのシルエット化
        #鍵との比較=>poseWhitePixリストに追加
        poseAve = poseWhitePix/frame_count
        #ポーズシルエット開錠の判定
        #リストの平均値取得
        if poseAve < j:
            pose_key = True
            #開錠処理
            print('ポーズ認証')
            print('open')
            break
        else:
            pose_key = False
            print('ポーズ不認証')
            print('close')
            marker_key = False
            getFrame_flag = False
            frame_count = 0
            poseWhitePix = 0
    cv2.imshow('frame',frame)

    key = cv2.waitKey(30)
    if key == ord('q'):
        break
    elif key == ord('s'):
        getFrame_flag = True

cv2.destroyAllWindows()
cam.release()
