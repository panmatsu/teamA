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
    color_1 = extract_color(frame, 340, 20, 50, 75)  #red
    #cv2.imshow("color_1", color_1)
    # 画像の平滑化(メディアンフィルター)
    median = cv2.medianBlur(color_1, 5)
    #cv2.imshow("median", median)
    
    #円検出
    #############  パラメーターを適切な値にする必要あり  ##############
    circles = cv2.HoughCircles(median,cv2.HOUGH_GRADIENT,3,20,param1=50,param2=80,minRadius=10,maxRadius=200)
    if circles is not None:
        # 円が見つかった
        print("D::detect_red_circle.py:: detected!! ")
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:

            # positionListに円中心のXYを代入
            positionList.append(i[0])
            positionList.append(i[1])
            
            # 円の描画
            #cv2.circle(frame,(i[0],i[1]),1,(255,255,0),2)
        
    else:
        # 円が見つからなかった
        print("D::detect_redcircle::　NO  CIRCLE ")
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
    #cap = cv2.VideoCapture("marker_key.avi")
    cap = cv2.VideoCapture(0)
    while True:
        # フレーム読み込み
        ret, img = cap.read() 
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




