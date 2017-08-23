# http://lang.sist.chukyo-u.ac.jp/classes/OpenCV/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html
# http://qiita.com/daxanya1/items/85f5e17ecc1203f756ad
# https://www.blog.umentu.work/python-opencv3%E3%81%A7%E3%83%9E%E3%82%B9%E3%82%AF%E5%87%A6%E7%90%86%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B%EF%BC%88%E3%81%8A%E3%81%BE%E3%81%91%E3%81%82%E3%82%8A%EF%BC%89/

import cv2
import numpy as np
import sys

#cam = cv2.VideoCapture(0)

if __name__=='__main__':
    if len(sys.argv) < 3:
        print('filename is not specified.')
        sys.exit(1)

cap = cv2.imread(sys.argv[1],0)
frame = cv2.imread(sys.argv[2],0)


fname = 'backSub.png'
fgmask = cv2.absdiff(frame,cap)


t = 25
ret, binal = cv2.threshold(fgmask, t, 255, cv2.THRESH_BINARY)

kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(binal,kernel,iterations = 1)

opening = cv2.morphologyEx(binal, cv2.MORPH_OPEN, kernel)
kernel = np.ones((5,5),np.uint8)
result = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)


cv2.imwrite('backgroud.png',result)

