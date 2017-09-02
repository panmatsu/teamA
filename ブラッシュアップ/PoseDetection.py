import cv2
import numpy as np

class PoseDetection:

    #２値化パラメータ
    t = 50
    #平滑化パラメータ
    n = 5
    #ノイズ消しパラメータ
    kernelo = np.ones((5,5),np.uint8)
    #穴埋めパラメータ
    kernelc = np.ones((5,5),np.uint8)

    #ポーズ判定ピクセル数
    j = 15000

    #ポーズピクセル平均値
    ave = 0

    #フレーム取得回数
    k = 10

    count = 0

    def __init__(self,ta,na,ja,ka):
        self.t = ta
        self.n = 5
        self.j = ja
        self.k = ka

    def cmp_pose(self,frame,back,key,log):
        log.write("フレーム取得\n")
        
        #グレイ化
        gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        #背景との差分
        fgmask = cv2.absdiff(gray,back)
        #2値化 
        ret, binal = cv2.threshold(fgmask, self.t, 255, cv2.THRESH_BINARY)
        #平滑下 
        binal = cv2.medianBlur(binal, self.n)
        #オープニング処理
        erosion = cv2.erode(binal,self.kernelo,iterations = 1)
        opening = cv2.morphologyEx(binal, cv2.MORPH_OPEN, self.kernelo)
        #クロージング処理
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, self.kernelc)
        
        #鍵との比較
        result = cv2.absdiff(closing,key)
        
        #name = 'diff'+str(self.count)+'.png' 
        #cv2.imwrite(name,result)

        #白ピクセル計算
        return cv2.countNonZero(result)

    def judge_pose(self,frame,back,key,log):
        if self.count < self.k:
            self.ave = self.cmp_pose(frame,back,key,log)
            self.count += 1
            return 0
        else:
            self.ave = self.ave/self.k
            log.write(str(self.ave)+"\n")
            if self.ave < self.j:
                log.write("pose key open\n")
                return 1
            else:
                log.write("pose key close\n")
                self.ave = 0
                self.count = 0
                return 2
                
            
