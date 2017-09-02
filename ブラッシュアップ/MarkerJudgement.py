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

import MarkerDetection

class MarkerJudgement():
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
    def set_lock_position(self,l_lt_x, l_lt_y, l_rb_x, l_rb_y, r_lt_x, r_lt_y, r_rb_x, r_rb_y):
        
        # かぎ左マーカーの座標リスト
        #global lock_position_left
        # 左マーカーの左上ｘ
        self.lock_position_left[0] = l_lt_x
        # 左マーカーの左上ｙ
        self.lock_position_left[1] = l_lt_y
        # 左マーカーの右下ｘ
        self.lock_position_left[2] = l_rb_x
        # 左マーカーの右下ｙ
        self.lock_position_left[3] = l_rb_y
        
        
        # かぎ右マーカーの座標リスト
        #global lock_position_right
        # 右マーカーの左上ｘ
        self.lock_position_right[0] = r_lt_x
        # 右マーカーの左上ｙ
        self.lock_position_right[1] = r_lt_y
        # 右マーカーの右下ｘ
        self.lock_position_right[2] = r_rb_x
        # 右マーカーの右下ｙ
        self.lock_position_right[3] = r_rb_y

    #############  新::マーカー判定  ################ 
    ##
    ## すべての座標が、かぎ座標内にあるか判定する
    ## 
    ################################################
    def judge_marker(self,md,img,log):
        
        # ****リスト更新**** 
        md.detect_red_circle(img,log)
        # detect_red_circle.pyから円の中心座標List(x,y)を持ってくる 
        positionList = md.positionList
        
        # 座標リストの大きさが2以下だった場合Falseを返却 
        # 十分なサンプルがないので 
        if len(positionList) < 2:
            return False
        
        # 鍵マーカー認識領域描画
        self.lock_position_left
        self.lock_position_right
        # 左：ピンク
        cv2.rectangle(img, (self.lock_position_left[0],self.lock_position_left[1]),(self.lock_position_left[2],self.lock_position_left[3]),(255,0,255), 2)
        # 右：水色 
        cv2.rectangle(img, (self.lock_position_right[0],self.lock_position_right[1]),(self.lock_position_right[2],self.lock_position_right[3]),(255,255,0), 2)
        #cv2.imshow("Judge",img)  


        # 左鍵マーカー完了フラグ
        leftFlag = False
        # 右鍵マーカー完了フラグ  
        rightFlag = False
        # 繰り返しカウント
        cnt = 0
        # 座標リストと鍵マーカーを比較する 
        while cnt < len(positionList)-1:
            
            if self.lock_position_left[0] < positionList[cnt]:
                # 左上ｘより大きく 
                if self.lock_position_left[2] > positionList[cnt]:
                    #右下xより小さく
                    if self.lock_position_left[1] < positionList[cnt+1]:
                        #左上ｙより大きく
                        if self.lock_position_left[3] > positionList[cnt+1]:
                            #右下ｙより小さいなら
                            #print("OKOKOKOKOKOKOKOKOKOKOKOKleft")  
                            log.write("left marker is in area\n")
                            leftFlag = True
            if self.lock_position_right[0] < positionList[cnt]:
                # 左上ｘより大きく 
                if self.lock_position_right[2] > positionList[cnt]:
                    #右下xより小さく
                    if self.lock_position_right[1] < positionList[cnt+1]:
                        #左上ｙより大きく
                        if self.lock_position_right[3] > positionList[cnt+1]:
                            #右下ｙより小さいなら
                            #print("OKOKOKOKOKOKOKOKOKOKOKOKRight") 
                            log.write("right marker is in area\n")
                            rightFlag = True
                        
            # 両方フラグがtrueになったなら認識OK 
            if rightFlag == True & leftFlag == True:
                return True,img
        
            cnt += 2
        
        return False,img
