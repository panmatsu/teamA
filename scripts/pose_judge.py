
import cv2
import numpy as np
import sys

if __name__=='__main__':
    if len(sys.argv) < 3:
        print('Usage: $python filename img1 img2')
        sys.exit(1)

#コマンドラインからグレー画像を取得
frame = cv2.imread(sys.argv[1],0)
key = cv2.imread(sys.argv[2],0)

#差分処理
result = cv2.absdiff(frame,key)

#(0,0,0)でない部分の面積
white = cv2.countNonZero(result)

#判定
print(white)
if white < 7000:
    print('open!')
else:
    print('....')
cv2.imwrite('judge.png',result)

