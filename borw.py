# -*- coding: utf-8 -*-
import cv2
import numpy as np

white = 0

# 画像取得
img = cv2.imread("pict.png",cv2.IMREAD_GRAYSCALE)

# [0,0,0]でない部分の計算
white = cv2.countNonZero(img)

print(white)