import cv2 
import numpy as np 
import os
import sys


def cmp_pose(frame,frame_count,back,key_pose,log):   

    #２値化のパラメータ
    t = 50
    # 平滑下のパラメータ
    n = 5
    #ノイズ消しのパラメータ
    kernelo = np.ones((5,5),np.uint8)
    #穴埋めパラメータ
    kernelc = np.ones((5,5),np.uint8)

    
    #print('フレーム取得')
    #filename = "doc\""+'frame' + str(frame_count) + '.png'
    #cv2.imwrite(filename,frame)
    log.write("フレーム取得\n")
    #グレイ化
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    #背景との差分
    fgmask = cv2.absdiff(gray,back)
    #2値化
    ret, binal = cv2.threshold(fgmask, t, 255, cv2.THRESH_BINARY)
    binal = cv2.medianBlur(binal, n)
    erosion = cv2.erode(binal,kernelo,iterations = 1)
    #オープニング処理
    opening = cv2.morphologyEx(binal, cv2.MORPH_OPEN, kernelo)
    #クロージング処理
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelc)
    #平滑下
    result = cv2.absdiff(closing,key_pose)
    #name = 'diff'+str(frame_count)+'.png'
    #cv2.imwrite(name,result)

    return cv2.countNonZero(result)


def judge_pose(poseWhitePix,frame_count,log):
    #ポーズ判定ピクセル
    j = 15000

    poseAve = poseWhitePix/frame_count
    log.write(str(poseAve)+"\n")
    #ポーズシルエット開錠の判定
    #リストの平均値取得
    if poseAve < j:
        return True
    else:
        return False


##################--main--##################
if __name__ == '__main__':
    cam = cv2.VideoCapture(sys.argv[1])
    #背景画像
    back = cv2.imread('back.png',0)
    #現時点では鍵の探索は未実装
    #鍵
    key_pose = cv2.imread(sys.argv[2],0)

    getFrameFlag = False
    white = 0
    count = 0
    
    while(1):
        ret, frame = cam.read()
        if ret == False:
            break        
        if getFrameFlag == True and count < 10:
            white += cmp_pose(frame,count)
            count = count + 1
        if count == 10:
            if judge_pose(white,count) == True:
                print('ok')
                break
            else:
                print('NG')
                break
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
        elif key == ord('s'):
            getFrameFlag = True
        cv2.imshow('frame',frame)
    cv2.destroyAllWindows()
    cam.release()

        
    

            
            

