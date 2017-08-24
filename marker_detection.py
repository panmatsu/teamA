# 参考サイト
# http://qiita.com/sbtseiji/items/6438ec2bf970d63817b8

import cv2
import numpy as np
from matplotlib import pyplot as pyplot


def detect_marker():

    img_rgb = cv2.imread('MarioVSKuppa.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread('fire.jpg', 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 4)
    cv2.imshow("Image", img_rgb) 
    while True:
        # qを押したら終了。
        k = cv2.waitKey(1)
        if k == ord('q'):
            break



if __name__ == '__main__':
    detect_marker()

