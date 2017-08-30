# 参考サイト
# http://qiita.com/sbtseiji/items/6438ec2bf970d63817b8
# http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
# https://matplotlib.org/users/installing.html # matplotlibのインストール
#

import cv2
import numpy as np
from matplotlib import pyplot as pyplot


    
loc = None

def get_position():
    plist = [-1]
    for pt in zip(*loc[::-1]):
        if plist[0] == -1:
            plist[0] = pt[0]
        else:
            plist.append(pt[0])
    return plist

####  マーカー検知  ####
def detect_marker(img_rgb,template):
    ## 元画像読み込み
    #img_rgb = cv2.imread('7.png')
    # グレースケール化し、保存
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


    ## テンプレート画像読み込み
    #template = cv2.imread('hand.pn
    # 画像サイズ取得
    w, h = template.shape[::-1]

    # テンプレートマッチング
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # マッチ度
    threshold = 0.7
    # マッチ度より高ければ場所保存
    # グローバル指定
    global loc
    loc = np.where( res >= threshold)

    cnt = 0

    # マッチした数だけ
    for pt in zip(*loc[::-1]):
        #print("左上:"+str(pt[0]))
        # 左上座標と右下座標から四角形表示
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 4)
        cnt += 1

    # マッチしなかったら
    if cnt == 0:
        #print("Nothing")
        return False


    # 画像表示
    cv2.imshow("Image", img_rgb) 
    while True:
        # qを押したら終了。
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    return True



if __name__ == '__main__':
    detect_marker()
    positionList = get_position()
    #print(len(positionList))

