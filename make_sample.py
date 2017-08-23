# http://lang.sist.chukyo-u.ac.jp/classes/OpenCV/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html
# http://qiita.com/daxanya1/items/85f5e17ecc1203f756ad
# https://www.blog.umentu.work/python-opencv3%E3%81%A7%E3%83%9E%E3%82%B9%E3%82%AF%E5%87%A6%E7%90%86%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B%EF%BC%88%E3%81%8A%E3%81%BE%E3%81%91%E3%81%82%E3%82%8A%EF%BC%89/

import cv2
import numpy as np
import sys

#cam = cv2.VideoCapture(0)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print('filename is not specified.')
        sys.exit(1)

cap = cv2.VideoCapture(sys.argv[1])

count = 0
num = 1
try:
    while(1):
        count = (count + 1) % 10
        ret, frame = cap.read()
        if ret == False:
            break

        if count == 0:
            fname = 'back' + str(num) + ".png"
            cv2.imwrite(fname,frame)
            num = num + 1
finally:
    cv2.destroyAllWindows()


