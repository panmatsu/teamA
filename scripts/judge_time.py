###############################################
##                                       
##  何秒間か判定する
##
##############################################
import time

# 判定開始時刻
start = None
# 判定時間
result = 0.0

# 引数
# int sec: 判定したい時間(秒)
def judge_time(sec):

    global start
    if start is None:
        # スタートが設定されてない場合
        # 開始時刻設定
        start = time.time()

    global result
    # 現在時刻 ー スタートタイム
    result = time.time() - start

    # 計算時間が判定時刻を越えたなら
    if result > sec:
        ###  判定終了  ###
        # 値のリセット
        start = None
        result = None
        return True

    return False
        

############### How to use #############
##if __name__ == '__main__':
##   while True:
##        if judge_time() == True:
##            break
##    print("FINISH!")
