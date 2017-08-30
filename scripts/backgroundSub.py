
import cv2
import numpy as np
import sys

if __name__=='__main__':
    if len(sys.argv) < 3:
        print('Usage: $python filename img1 img2')
        sys.exit(1)

#コマンドラインからグレー画像を取得
cap = cv2.imread(sys.argv[1],0)
frame = cv2.imread(sys.argv[2],0)

#差分処理
fgmask = cv2.absdiff(frame,cap)

#２値化の閾値
t = 50
ret, binal = cv2.threshold(fgmask, t, 255, cv2.THRESH_BINARY)

# 平滑下
binal = cv2.medianBlur(binal, 5)

#ノイズ消しのパラメータ
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(binal,kernel,iterations = 1)
#ノイズ処理
opening = cv2.morphologyEx(binal, cv2.MORPH_OPEN, kernel)

#穴埋めパラメータ
kernel = np.ones((5,5),np.uint8)
#穴埋め処理
result = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

#(0,0,0)でない部分の面積
white = white = cv2.countNonZero(result)
print(white)

cv2.imwrite('backgroud.png',result)

