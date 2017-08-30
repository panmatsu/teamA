# -*- coding: utf-8 -*-
import cv2
import numpy as np

def main():

    th = 50    # 差分画像の閾値
    
    # ポーズの動画
    cap = cv2.VideoCapture("a.avi")

    # 背景の動画
    bgcap = cv2.VideoCapture('b.avi')


    while(True):
        # 背景動画のフレームの取得
        ret,bgframe = bgcap.read()
        if ret == False:
            break
        # グレースケール化
        bg = cv2.cvtColor(bgframe, cv2.COLOR_BGR2GRAY)

        # ポーズ動画のフレームの取得
        ret,frame = cap.read()
        if ret == False:
            break
        # グレースケール化
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 差分の絶対値計算
        mask = cv2.absdiff(gray, bg)
        
        # 差分画像を二値化しマスク画像を算出
        mask[mask < th] = 0
        mask[mask >= th] = 255
        
        # 平滑下
        median = cv2.medianBlur(mask, 5)

        # マスク画像を表示
        cv2.imshow("Mask", median)

        # qキーが押されたら途中終了
        key = cv2.waitKey(30)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()