###############################################
##                                       
##  指定枠内にマーカーが存在するか判定する  
## 
##  引数:img(画像)
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
lock_position_right = [240,110,285,150]
lock_position_left  = [420,260,473,300]


# かぎ位置設定
# 引数は上(line:13)のマーカーの鍵位置参照
def set_lock_position(l_lt_x, l_lt_y, l_rb_x, l_rb_y, r_lt_x, r_lt_y, r_rb_x, r_rb_y):

    
    # かぎ左マーカーの座標リスト
    global lock_position_left
    # 左マーカーの左上ｘ
    lock_position_left[0] = l_lt_x
    # 左マーカーの左上ｙ
    lock_position_left[1] = l_lt_y
    # 左マーカーの右下ｘ
    lock_position_left[2] = l_rb_x
    # 左マーカーの右下ｙ
    lock_position_left[3] = l_rb_y


    # かぎ右マーカーの座標リスト
    global lock_position_right
    # 右マーカーの左上ｘ
    lock_position_right[0] = r_lt_x
    # 右マーカーの左上ｙ
    lock_position_right[1] = r_lt_y
    # 右マーカーの右下ｘ
    lock_position_right[2] = r_rb_x
    # 右マーカーの右下ｙ
    lock_position_right[3] = r_rb_y


#############  新::マーカー判定  ################
## 
## すべての座標が、かぎ座標内にあるか判定する
##
#################################
def judge_marker(img,log):

    # ****リスト更新****
    detect_red_circle(img,log)
    # detect_red_circle.pyから円の中心座標List(x,y)を持ってくる
    positionList = get_position()

    # 座標リストの大きさが2以下だった場合Falseを返却
    # 十分なサンプルがないので
    if len(positionList) < 2:
        return False

    # 鍵マーカー認識領域描画
    global lock_position_left
    global lock_position_right
    # 左：ピンク
    cv2.rectangle(img, (lock_position_left[0],lock_position_left[1]),(lock_position_left[2],lock_position_left[3]),(255,0,255), 2)
    # 右：水色
    cv2.rectangle(img, (lock_position_right[0],lock_position_right[1]),(lock_position_right[2],lock_position_right[3]),(255,255,0), 2)
    #cv2.imshow("Judge",img)

    
    # 左鍵マーカー完了フラグ
    leftFlag = False
    # 右鍵マーカー完了フラグ
    rightFlag = False
    # 繰り返しカウント
    cnt = 0
    # 座標リストと鍵マーカーを比較する
    while cnt < len(positionList)-1:

        if lock_position_left[0] < positionList[cnt]:
            # 左上ｘより大きく
            if lock_position_left[2] > positionList[cnt]:
                #右下xより小さく
                if lock_position_left[1] < positionList[cnt+1]:
                    #左上ｙより大きく
                    if lock_position_left[3] > positionList[cnt+1]:
                        #右下ｙより小さいなら
                        #print("OKOKOKOKOKOKOKOKOKOKOKOKleft")
                        log.write("left marker is in area\n")
                        leftFlag = True

        if lock_position_right[0] < positionList[cnt]:
            # 左上ｘより大きく
            if lock_position_right[2] > positionList[cnt]:
                #右下xより小さく
                if lock_position_right[1] < positionList[cnt+1]:
                    #左上ｙより大きく
                    if lock_position_right[3] > positionList[cnt+1]:
                        #右下ｙより小さいなら
                        
                        #print("OKOKOKOKOKOKOKOKOKOKOKOKRight")
                        log.write("right marker is in area\n")
                        rightFlag = True

        # 両方フラグがtrueになったなら認識OK
        if rightFlag == True & leftFlag == True:
            return True
        # 
        cnt += 2
    
    
    return False










####  旧::マーカー判定  ####
#全体座標リストから左右リストに振り分ける
#左右リストは鍵の中に入ってるか確認
def old_judge_marker(img):

    # ****リスト更新****
    detect_red_circle(img)
    # detect_red_circle.pyから円の中心座標List(x,y)を持ってくる
    positionList = get_position()

    # 座標リストの大きさが2以下だった場合Falseを返却
    # 十分なサンプルがないので
    if len(positionList) < 2:
        return False

    # ただ左右すべてのXとYだけに振り分けるリスト

    XList = []
    YList = []


    # 座標リストからXとYListに振り分ける
    for i in range(len(positionList)):
        if i%2 == 0:
            # 偶数のとき
            # X座標リストに追加する

            XList.append(positionList[i])
        else:
            # 奇数のとき
            # Y座標リストに追加する

            YList.append(positionList[i])
    
    # XとYの平均を計算
    xAve = sum(XList)/len(XList)
    yAve = sum(YList)/len(YList)

    #print("xAve:"+str(xAve))
    #print("yAve:"+str(yAve))

    # Listをそれぞれ小さい順に並び替える
    XList.sort()
    YList.sort()

    ############ 左右で分かれる場所を確認する  ############
    # Xの差とYの差が大きいほうを比較対象にする
    diff_x = XList[len(XList)-1] - XList[0]
    diff_y = YList[len(YList)-1] - YList[0]
    cnt = 0
    if diff_x > diff_y :
        # Xの差が大きければXを比較対象

        while cnt < len(XList)-1:
            # 平均を超えたcntで終了
            if XList[cnt] > xAve:
                break
            cnt += 1
    else:
        # Yの差が大きければYを比較対象
        while cnt < len(YList)-1:
            # 平均を超えたcntで終了
            if YList[cnt] > yAve:
                break
            cnt += 1
    
    

    #print("Xlist[cnt-1]:"+str(XList[cnt-1]))
    #print("Ylist[cnt-1]:"+str(YList[cnt-1]))
    #print("わかれめ")
    #print("XList[cnt]:"+str(XList[cnt]))
    #print("YList[cnt]:"+str(YList[

        
    # 左右のマーカーの位置座標
    RightList = []
    LeftList  = []
    #rint("len_x:"+str(len(XList)))
    #print("len_y:"+str(len(YList)))

    # 左右マーカーの左上座標特定終了
    if XList[cnt-1] < xAve:
        # 分け目前が平均より小さければ左マーカー
        LeftList.append(XList[cnt-1])
        LeftList.append(YList[cnt-1])
        RightList.append(XList[cnt])
        RightList.append(YList[cnt])
    else:
        # 分け目後が平均より大きければ右マーカー
        RightList.append(XList[cnt-1])
        RightList.append(YList[cnt-1])
        LeftList.append(XList[cnt])
        LeftList.append(YList[cnt])
    
    # 左：ピンク
    cv2.circle(img,(LeftList[0],LeftList[1]),1,(255,0,255),2)
    # 右：水色
    cv2.circle(img,(RightList[0],RightList[1]),1,(255,255,0),2)
    #cv2.imshow("capture", img)
    
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
if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    mode = 0

    while(1):
        ret, frame = cap.read()

        if mode == 0:
            if detect_red_circle(frame) == True:
                mode += 1
        elif mode == 1:
            if judge_marker(frame) == True:
                mode += 1
        else:
            print("判定終了")
            break

                # キーボード確認
        key = cv2.waitKey(10)
        if key == ord('q'):
            # Qが押されたら終了
            break
    
    cv2.destroyAllWindows()
    cap.release()

    ##  test  ##
#    img = cv2.imread('red_circles.png')
#    if detect_red_circle(img) == True :
#        print("TRUE")
#    
#    if judge_marker() == True:
#        print("判定成功")
#    else:
#        print("判定失敗")
