import cv2
import numpy as np

def detect_circle():
    cam = cv2.VideoCapture(0)
    flag = False
    while True:
        ret, img = cam.read()

        img = cv2.medianBlur(img,5)
        cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # param1:
        circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=80,minRadius=10,maxRadius=100)
        if circles is not None:
            print("*D::Detect!*")
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # 囲み線
                cv2.circle(img,(i[0],i[1]),i[2],(255,255,0),2)

        cv2.imshow('image',img)
        key = cv2.waitKey(10)
        

        if key is ord('q'):
            break

    cv2.destroyAllWindows()
    cam.release()



if __name__ == '__main__':
    detect_circle()