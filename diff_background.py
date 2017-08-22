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
cv2.namedWindow(WINDOW_ORG)
cv2.namedWindow(WINDOW_BACK)
cv2.namedWindow(WINDOW_DIFF)

# 元ビデオファイル読み込み
mov_org = cv2.VideoCapture('pose.avi')

# 最初のフレーム読み込み
has_next, i_frame = mov_org.read()

# 背景フレーム
back_frame = np.zeros_like(i_frame, np.float32)

# 変換処理ループ
while has_next == True:
    # 入力画像を浮動小数点型に変換
    f_frame = i_frame.astype(np.float32)

    # 差分計算
    diff_frame = cv2.absdiff(f_frame, back_frame)

    # 背景の更新
    cv2.accumulateWeighted(f_frame, back_frame, 0.025)

    # フレーム表示
    cv2.imshow(WINDOW_ORG, i_frame)
    cv2.imshow(WINDOW_BACK, back_frame.astype(np.uint8))
    cv2.imshow(WINDOW_DIFF, diff_frame.astype(np.uint8))

    # Escキーで終了
    key = cv2.waitKey(INTERVAL)
    if key == ESC_KEY:
        break

    # 次のフレーム読み込み
    has_next, i_frame = mov_org.read()

# 終了処理
cv2.destroyAllWindows()
mov_org.release()