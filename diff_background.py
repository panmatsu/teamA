import cv2
import numpy as np

# 定数定義
ESC_KEY = 27     # Escキー
INTERVAL= 33     # インターバル
FRAME_RATE = 30  # fps

WINDOW_ORG = "org"
WINDOW_BACK = "back"
WINDOW_DIFF = "diff"


# ウィンドウの準備
cv2.namedWindow(WINDOW_DIFF)

# カーネル設定
kernel = np.ones((2,2),np.uint8)



# 背景ビデオファイル読み込み
cam1 = cv2.VideoCapture('bg.avi')
# グレースケール
back_frame = cv2.cvtColor(cam1.read()[1], cv2.COLOR_RGB2GRAY)



# 比較ビデオファイル読み込み
cam = cv2.VideoCapture('pose.avi')
# グレースケール化
org_frame = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)



# 変換処理ループ
while True:

    # 差分計算
    diff_frame = cv2.absdiff(org_frame, back_frame)

    diff_frame = cv2.morphologyEx(diff_frame, cv2.MORPH_OPEN, kernel)

    ### フレーム表示 ###
    ## 差分動画表示
    cv2.imshow(WINDOW_DIFF, diff_frame)

    # Escキーで終了
    key = cv2.waitKey(INTERVAL)
    if key == ESC_KEY:
        break

    # 次のフレーム読み込み
    org_frame = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

# 終了処理
cv2.destroyAllWindows()
