# -*- codeing: utf-8 -*-
###############################################
##                                       
##  画像内に赤円があるか確認し、あったら座標を保存 
## 
##  引数:img(画像)
##
##  return:(bool)true or false
##
##############################################
import cv2
import numpy as np
from matplotlib import pyplot as plt


def nothing(x):
    pass

# メンバ変数
positionList = [-1]

# ---private---
# extract_color(画像, 色相閾値low, 色相閾値high, 彩度閾値, 明度閾値)
def extract_color(src, h_low, h_high, s_st, v_st):

    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    # 赤はhが350°-10°
    if h_low > h_high:
        # threshold(画像, 閾値, 最大値, 処理タイプ)
        ## BINARY:     閾値より大きい値は最大値,他は0
        ## BINARY_INV: 閾値より大きい値は0,他は最大値
        ret, h_dst_1 = cv2.threshold(h, h_low, 255, cv2.THRESH_BINARY)
        ret, h_dst_2 = cv2.threshold(h, h_high, 255, cv2.THRESH_BINARY_INV)

        dst = cv2.bitwise_or(h_dst_1, h_dst_2)

    else:
        ## TOZERO:     閾値より大きい値はそのまま,他は0
        ## TOZERO_INV: 閾値より大きい値は0,他はそのまま
        ret, dst = cv2.threshold(h, h_low, 255, cv2.THRESH_BINARY) #閾値以下を0に
        ret, dst = cv2.threshold(dst, h_high, 255, cv2.THRESH_BINARY_INV) #閾値以上を0に

        ret, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY)

    ret, s_dst = cv2.threshold(s, s_st, 255, cv2.THRESH_BINARY)
    ret, v_dst = cv2.threshold(v, v_st, 255, cv2.THRESH_BINARY)

    dst = cv2.bitwise_and(dst, s_dst)
    dst = cv2.bitwise_and(dst, v_dst)

    return dst


# +++public +++
# 円の中心位置座標(X,Y)をリストで返却
def get_position():
    global positionList
    return positionList


cv2.namedWindow("Adjust")
# create trackbar
# trackbarName, windowName, 初期値, 最大数, onChange
cv2.createTrackbar('h_low','Adjust',0,180,nothing)
cv2.createTrackbar('h_high','Adjust',0,180,nothing)
cv2.createTrackbar('s_st','Adjust',0,100,nothing)
cv2.createTrackbar('v_st','Adjust',0,100,nothing)
track = np.zeros((300,512,3),np.uint8)




# +++public+++
#########################################
#########    　赤円検出      #############
#########################################
##  赤い円を検出し、中心点を返却 ##
def detect_red_circle(frame):

    global positionList
    del positionList[:]
    
    #cv2.imshow("frame", frame)
    

    # 取りたい色をHSVでパラメータ設定
    # (画像、最低色相角、最高色相角、彩度閾値、明度閾値)
    #############  パラメーターを適切な値にする必要あり  ##############

    # ****  赤  ****
    #color_1 = extract_color(frame, 350, 20, 70, 70)
    
    # ****  黄  ****
    #   割と精度いい
    # 昔の黄色のパラメーター
    # color_1 = extract_color(frame, 50, 70, 70, 70)
    
    cv2.imshow("Adjust",track)

    h_low = cv2.getTrackbarPos("h_low","Adjust")
    h_high = cv2.getTrackbarPos("h_high","Adjust")
    s_st = cv2.getTrackbarPos("s_st","Adjust")
    v_st = cv2.getTrackbarPos("v_st","Adjust")



    ######  最終決定か  #############
    # 赤対応　ある程度のボールの影にも強い
    color_1 = extract_color(frame, 163, 0, 100, 68)


    # ****  青  ****
    #color_1 = extract_color(frame, 190, 210, 80, 80)

    # ****  ターコイズ  ****
    #color_1 = extract_color(frame, 160, 180, 60, 75)

    #cv2.imshow("color_1", color_1)

    # 画像の平滑化(メディアンフィルター)
    median = cv2.medianBlur(color_1, 5)
    cv2.imshow("Before", median)

    # ８近傍フィルター
    neiborhood8 = np.array([[1,1,1],
                            [1,1,1],
                            [1,1,1]],np.uint8)
    # フィルターによる膨張処理                            
    img_dilation = cv2.dilate(median, neiborhood8,iterations=1)
    #cv2.imshow("After",img_dilation)

    median = img_dilation

    kernel = np.ones((5,5),np.uint8)
    # ノイズ除去
    median = cv2.morphologyEx(median, cv2.MORPH_OPEN, kernel)
    cv2.imshow("dst",median)

    ##　重心求める
    imgEdge, contours, hierarchy = cv2.findContours(median,1,2)
    #print(str(len(contours)))
    
    # 真っ黒画像だった場合False
    if len(contours) == 0:
        return False
    cnt = contours[0]
    M = cv2.moments(cnt)
    #print(str(M))
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    #print("cx:"+str(cx)+"cy:"+str(cy))



    #円検出
    #############  パラメーターを適切な値にする必要あり  ##############
    circles = cv2.HoughCircles(median,cv2.HOUGH_GRADIENT,3,20,param1=50,param2=80,minRadius=1,maxRadius=50)
    if circles is not None:
        # 円が見つかった
        #print("D::detect_red_circle:: detected!! ")
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:

            # positionListに円中心のXYを代入
            positionList.append(i[0])
            positionList.append(i[1])
            
            # 円の描画
            cv2.circle(frame,(i[0],i[1]),1,(255,255,0),2)
        
    else:
        # 円が見つからなかった
        #print("D::detect_red_circle::　NO  CIRCLE ")
        #while True:
        #    # qを押したら終了。
        #    k = cv2.waitKey(1)
        #    if k == ord('q'):

        return False

    
    #cv2.imshow("capture", frame)


    #while True:
        # qを押したら終了。
    #    k = cv2.waitKey(1)
    #    if k == ord('q'):
    #        break
        
    #cv2.destroyAllWindows()

    return True


if __name__ == '__main__':
    # ファイル読み込み
    #cap = cv2.VideoCapture("hira_05.avi")
    cap = cv2.VideoCapture(0)
    while True:
        # フレーム読み込み
        ret, img = cap.read() 
        # フレームが終了したらおわり
        if img is None:
            break

        detect_red_circle(img)

        cv2.imshow("Img",img)
        
        # キーボード確認
        key = cv2.waitKey(10)
        if key == ord('q'):
            # Qが押されたら終了
            break

        #elif key == ord('j'):
            # Jが押されたら

    polist = get_position()

    print(len(polist))
    for i in polist:
        print(i)




