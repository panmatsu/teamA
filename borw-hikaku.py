# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 白面積の算出法定義
def equivalent_white(filename):
    white = 0
    # 画像取得
    img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)

    # [0,0,0]でない部分の計算
    white = cv2.countNonZero(img)

    return white

if __name__ == '__main__':
    dif = equivalent_white("pict.png") - equivalent_white("pict2.png")
    print(dif)
    
