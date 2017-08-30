#######################################
##                                   ##
##  動画ファイルから画像ファイルへ変換  ##
##                                   ##
#######################################
import numpy as np
import cv2
import sys



# ファイル読み込み
cap = cv2.VideoCapture(sys.argv[1])
# フレーム読み込み
ret, frame = cap.read()
cnt = 0

while(True):
    # フレームに何もないなら終了
    if frame is None:
        print("FINISH!!")
        break
    # グレースケール化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # イメージ表示
    cv2.imshow('frame',gray)

    # キーボード確認
    key = cv2.waitKey(1)
    if key == ord('q'):
        # Qが押されたら終了
        break
    elif key == ord('n'):
        # Nが押されたら次のフレーズへ
        ret, frame = cap.read()
    elif key == ord('s'):
        # Sが押されたら画像保存
        file_name = str(cnt) + ".png"
        cv2.imwrite(file_name, gray)
        cnt += 1
    

cap.release()
cv2.destroyAllWindows()