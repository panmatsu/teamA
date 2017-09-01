# -*- codeing: utf-8 -*-

import numpy as np
import sqlite3
import sys
import cv2
import shutil
import os


# コマンドラインより登録データ取得(id)
print("please write your ID >")
rnid = sys.stdin.readline()
nid = rnid.rstrip("\n")
# idが既存のものでないか確認
check = sqlite3.connect("dbkey.db", isolation_level=None)
sql = "select * from keyset where id ==" + str(nid)
ch = check.cursor()
ch.execute(sql)
number = 0
for row in ch:
    number = row[0]

if number == 0:
    pass
else:
    print("sorry, your id is already input.")
    sys.exit()

# コマンドラインより登録データ取得(id)
print("please write your name in English >")
rnname = sys.stdin.readline()
nname = rnname.rstrip("\n")

print("\nplease push key｢s｣, we need background picture!")

# 背景画像取得のためのカメラキャプチャ
cap = cv2.VideoCapture(1)
while(True):
    ret, frame = cap.read()
    if ret == False:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # グレースケール化

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'): # 終了
        print("you press key｢q｣, so finish this plogram.")
        sys.exit()
    elif key == ord('s'): # 保存
        file_name = "background.png"
        cv2.imwrite(file_name, gray) # 動画保存
        print("\nplease push key｢v｣, and pose for a key!\n if you come back, please push key｢q｣")
    elif key == ord('v'): # 動画保存開始
        output_filename = str(nid) + "_" + nname + ".avi"
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        four_cc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 30.0
        writer = cv2.VideoWriter(output_filename, four_cc, fps, (frame_width, frame_height))            # record first frame.
        writer.write(frame)

        while True:
            _, img = cap.read()
            if img is None:
                break
            cv2.imshow('capture', img)
            writer.write(img)
            k = cv2.waitKey(1)
            if k == ord('q'): # 撮影終了
                print("\nplease choose your pose_key!\n press｢n｣->next frame\n press｢s｣->save the image\n press｢q｣->finish")
                break
        
        cap.release()
        writer.release()
        cv2.destroyAllWindows()

# 上記撮影動画より好きな時点の画像をポーズ鍵とする
recap = cv2.VideoCapture(output_filename)
ret, poseframe = recap.read()

check_pose = "getfile"
while(True):
    if poseframe is None:
        print("FINISH!!")
        check_pose = "nofile"
        break

    gray = cv2.cvtColor(poseframe, cv2.COLOR_BGR2GRAY)
    cv2.imshow('poseframe',gray)
    pkey = cv2.waitKey(1)
    if pkey == ord('q'):
        print("you press key｢q｣, so finish this plogram.")
        sys.exit()
    elif pkey == ord('n'):
        ret, poseframe = recap.read()
    elif pkey == ord('s'):
        file_name = "gray_pose.png"
        cv2.imwrite(file_name,gray)
        break
recap.release()
cv2.destroyAllWindows()

if check_pose == "nofile":
    print("sorry, you don't press key｢s｣.")
    sys.exit()


    #### マーカー範囲指定
    #### 読み込むなりなんなりして取得、仮設定中
class mouseParam:
    def __init__(self, input_img_name):
        self.mouseEvent = {"x":None, "y":None, "event":None, "flags":None}
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)

    def __CallBackFunc(self, eventType, x, y, flags, userdata):
        
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType    
        self.mouseEvent["flags"] = flags    

    def getData(self):
        return self.mouseEvent

    def getEvent(self):
        return self.mouseEvent["event"]                

    def getFlags(self):
        return self.mouseEvent["flags"]                

    def getX(self):
        return self.mouseEvent["x"]  

    def getY(self):
        return self.mouseEvent["y"]  

    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])
        
print("\nplease click the upper-left on the left side marker.")
mark = []
count = ["lower-right on the left", "upper-left on the right", "lower-right on the right"]

def marker_get():
    num = 0
    if __name__ == "__main__":
        read = cv2.imread("gray_pose.png")
        window_name = "input window"
        cv2.imshow(window_name, read)
        mouseData = mouseParam(window_name)
        while 1:
            cv2.waitKey(20)
            #左クリックがあったら表示
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                click = mouseData.getPos()
                if click in mark:
                    pass
                else:
                    mark.append(click)
                    if num == len(count):
                        print("\nok, finished!")
                        break
                    else:
                        print("\nok, please click the", count[num], "side marker")
                        num = num + 1
                
        #右クリックがあったら終了
            elif mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN:
                break
    return mark            
    cv2.destroyAllWindows()

marker = marker_get()
if len(marker) == 4:
    pass
else:
    print("resset. you have one more chance.")
    marker = marker_get()
    if len(marker) == 4:
        pass
    else:
        print("sorry, your click is not true twice.")
        sys.exit()

left_ltx = marker[0][0]
left_lty = marker[0][1]
left_rbx = marker[1][0]
left_rby = marker[1][1]
right_ltx = marker[2][0]
right_lty = marker[2][1]
right_rbx = marker[3][0]
right_rby = marker[3][1]

#### ポーズの画像
backimg = cv2.imread("background.png")
keyimg = cv2.imread("gray_pose.png")
# 差分
fgmask = cv2.absdiff(backimg,keyimg)
# 画像処理
t = 50
ret, binal = cv2.threshold(fgmask, t, 255, cv2.THRESH_BINARY)
binal = cv2.medianBlur(binal, 5)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(binal,kernel,iterations = 1)
opening = cv2.morphologyEx(binal, cv2.MORPH_OPEN, kernel)
kernel = np.ones((5,5),np.uint8)
result = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

file_name = str(nid) + ".png"
cv2.imwrite(file_name, result)
pose = "img/" + file_name
shutil.move(file_name, pose)

os.remove(output_filename)
os.remove("background.png")
os.remove("gray_pose.png")

# 同フォルダ内のdbkey.dbのDBを展開
con = sqlite3.connect("dbkey.db", isolation_level=None)
sqlleft = str(left_ltx) + ", " + str(left_lty) + ", " + str(left_rbx) + ", " + str(left_rby)
sqlright = str(right_ltx) + ", " + str(right_lty) + ", " + str(right_rbx) + ", " + str(right_rby)
sql = "insert into keyset values (" + str(nid) + ", \'" + nname + "\', " + sqlleft + ", " + sqlright + ", \'" + pose + "\')"
# 実行
#print(sql)
con.execute(sql)
con.close()



