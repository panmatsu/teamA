# http://lang.sist.chukyo-u.ac.jp/classes/OpenCV/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html
# http://qiita.com/daxanya1/items/85f5e17ecc1203f756ad
# https://www.blog.umentu.work/python-opencv3%E3%81%A7%E3%83%9E%E3%82%B9%E3%82%AF%E5%87%A6%E7%90%86%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B%EF%BC%88%E3%81%8A%E3%81%BE%E3%81%91%E3%81%82%E3%82%8A%EF%BC%89/

import cv2
import numpy as np

cam = cv2.VideoCapture(0)
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))

# 赤色で塗りつぶした画像を作成
red = np.tile(np.uint8([255, 0, 255]), (height, width, 1))


# 背景差分取得
bsub = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
count = 0
try:
    while(1):
        count = (count + 1) % 10
        ret, frame = cam.read()
        if ret == False:
            break

        mask = bsub.apply(frame, learningRate=0.01)
        redfilter = cv2.bitwise_and(red, red, mask=mask)

        # 赤色で点滅させる
        if count < 5:
            result = cv2.bitwise_or(frame, redfilter)
        else:
            result = frame
    
        cv2.imshow('result', result)
        key = cv2.waitKey(30)
        if key == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    cam.release()

