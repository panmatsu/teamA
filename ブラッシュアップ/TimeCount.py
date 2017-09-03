import time
import cv2
import numpy as np

import PersonAuthentication
import MarkerJudgement
import MarkerDetection

#####################################
#特定動作を任意の時間続けているか判定
####################################

class TimeCount:

    #キープ秒数
    t = 3.0

    #秒数判定の最低フレーム
    f = 10

    start_time = 0.0

    frame_count = 0


    def __init__(self,ti,fr):
        
        self.t = ti
        self.f = fr

    def keep(self,ret,img):

        if ret == True and self.start_time == 0.0:
            self.start_time = time.time()

        if ret == True and self.start_time != 0.0:
            self.frame_count += 1

        if self.start_time != 0 and time.time()-self.start_time > self.t and self.frame_count > self.f:
            self.start_time = 0.0
            self.frame_count = 0
            return True

        elif self.start_time != 0 and time.time()-self.start_time > self.t and self.frame_count > self.f:
            self.start_time = 0.0
            self.frame_count = 0
            return False

        else:
            return False


