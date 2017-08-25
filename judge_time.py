###############################################
##                                       
##  3秒間か判定する
##
##############################################
import time

start = None
result = 0.0

# 引数
# int time: 判定したい時間
def judge_time():

    global start
    if start is None:
        start = time.time()

    global result

    result = time.time() - start

    if result > 3.0:
        start = None
        result = None
        return True
    return False
        

if __name__ == '__main__':

    ## How to use
    while True:
        if judge_time() == True:
            break
    print("FINISH!")
