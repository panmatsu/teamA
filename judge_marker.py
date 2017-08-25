###############################################
##                                       
##  指定枠内にマーカーが3秒間存在するか判定する  
##
##  return:(bool)true or false
##
##############################################
import cv2
import numpy as np
from detect_red_circle import *


#######   マーカーの鍵位置   #############
# 四角形座標内に存在するかで判定するための材料
# 0: 四角形左上X座標
# 1: 　〃　 〃 Y 〃
# 2: 四角形右下X座標
# 3: 　〃　 〃 Y 〃
##################################
lock_position_right = [0,0,700,700]
lock_position_left  = [0,0,700,700]


# かぎ位置設定
def set_lock_position(rt, rb, lt, lb):

    global lock_position_right
    # 右マーカーの上
    lock_position_right[0] = rt
    # 右マーカーの下
    lock_position_right[1] = rb

    global lock_position_left
    # 左マーカーの上
    lock_position_left[0] = lt
    # 左マーカーの下
    lock_position_left[1] = lb


####  Main::マーカー判定  ####
#全体座標リストから左右リストに振り分ける
#左右リストは鍵の中に入ってるか確認
def judge_marker():

    # detect_red_circle.pyから円の中心座標List(x,y)を持ってくる
    positionList = get_position()

    # ただ左右すべてのXとYだけに振り分けるリスト
    XList = [-1]
    YList = [-1]

    # 左右のマーカーの位置座標
    RightList = [-1]
    LeftList  = [-1]

    # 座標リストからXとYListに振り分ける
    for i in range(len(positionList)):
        if i%2 == 0:
            # 偶数のとき
            # X座標リストに追加する
            if XList[0] == -1:
                XList[0] = positionList[i]
            XList.append(positionList[i])
        else:
            # 奇数のとき
            # Y座標リストに追加する
            if YList[0] == -1:
                YList[0] = positionList[i]
            YList.append(positionList[i])
    
    # XとYの平均を計算
    xAve = sum(XList)/len(XList)
    yAve = sum(YList)/len(YList)
    print("xAve:"+str(xAve))
    print("yAve:"+str(yAve))

    # Listをそれぞれ小さい順に並び替える
    XList.sort()
    YList.sort()

    # 左右で分かれる場所を確認する
    # 課題：平均からXとYの値がより離れているほうを分岐条件にする
    cnt = 0
    while(1):   
        if YList[cnt] > yAve:
            break
        cnt += 1
    
    print("Xlist[cnt-1]:"+str(XList[cnt-1]))
    print("Ylist[cnt-1]:"+str(YList[cnt-1]))
    print("わかれめ")
    print("XList[cnt]:"+str(XList[cnt]))
    print("YList[cnt]:"+str(YList[cnt]))

    # 左右マーカーの左上座標特定終了
    if XList[cnt-1] < xAve:
        # 分け目前が平均より小さければ左マーカー
        LeftList[0] = XList[cnt-1]
        LeftList.append(YList[cnt-1])
        RightList[0] = XList[cnt]
        RightList.append(YList[cnt])
    else:
        # 分け目後が平均より大きければ右マーカー
        RightList[0] = XList[cnt-1]
        RightList.append(YList[cnt-1])
        LeftList[0]  = XList[cnt]
        LeftList.append(YList[cnt])
    
    # 左右マーカーと鍵マーカーを比較する
    leftFlag = False
    rightFlag = False
    if lock_position_left[0] < LeftList[0]:
        # 左上ｘより大きく
        if lock_position_left[2] > LeftList[0]:
            #右下xより小さく
            if lock_position_left[1] < LeftList[1]:
                #左上ｙより大きく
                if lock_position_left[3] > LeftList[1]:
                    #右下ｙより小さいなら
                    leftFlag = True

    if lock_position_right[0] < RightList[0]:
        # 左上ｘより大きく
        if lock_position_right[2] > RightList[0]:
            #右下xより小さく
            if lock_position_right[1] < RightList[1]:
                #左上ｙより大きく
                if lock_position_right[3] > RightList[1]:
                    #右下ｙより小さいなら
                    rightFlag = True
    
    if rightFlag == True & leftFlag == True:
        return True
    return False



############################### Test  #################
##if __name__ == '__main__':


    ##  test  ##
    img = cv2.imread('a.png')
    if detect_red_circle(img) == True :
        print("TRUE")
    
   if judge_marker() == True:
        print("判定成功")
    else:
        print("判定失敗")
