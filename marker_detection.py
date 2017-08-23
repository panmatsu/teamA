# 参考サイト
# http://qiita.com/sbtseiji/items/6438ec2bf970d63817b8

import cv2
import numpy as np

def detect_marker():
    cam = cv2.VideoCapture(0)
    while True:
        ret, img = cam.read()



        # 表示
        cv2.imshow("Image", img)

        
        key = cv2.waitKey(10)
        if key is ord('q'):
            break

    cv2.destroyAllWindows()
    cam.release()



if __name__ == '__main__':
    detect_marker()

