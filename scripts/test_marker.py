
from judge_marker import *

if __name__ == '__main__':

    # ファイル読み込み
    cap = cv2.VideoCapture('video_06.avi')
    while True:

        # フレーム読み込み
        ret, frame = cap.read()
        # フレームに何もないなら終了
        if frame is None:
            print("FINISH!!")
            break
        judge_marker(frame)
        # キーボード確認
        key = cv2.waitKey(1)
        if key == ord('q'):
            # Qが押されたら終了
            break
    print("FINISH!")
