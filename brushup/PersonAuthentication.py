import cv2
import numpy as np

class PersonAuthentication():
    
    #HOG特徴量計算(体)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'winStride':(8,8),'padding':(32,32),'scale':1.05}

    #カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

    #枠の色
    face_color = (255,0,0)
    body_color = (0,255,0)

    def personDetect(self,frame,log):
        
        human,r = self.hog.detectMultiScale(frame,**self.hogParams)
        face = self.cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        
        if len(human) != 0:
            for(x,y,w,h) in human:
                cv2.rectangle(frame,(x,y),(x+w,y+h),self.body_color,3)
            log.write("detect dody\n")
        if len(face) != 0:
            for rect in face:
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), self.face_color, thickness=2)
            log.write("detect face\n")
    
        if len(human) != 0 and len(face) != 0:
            log.write("detect person\n")
            return (True,frame)
        else:
            log.write("detect person\n")
            return (False,frame)
