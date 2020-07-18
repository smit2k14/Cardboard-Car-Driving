import numpy as np
import cv2
import pyautogui
import time
from imutils.video import VideoStream

RIGHT = -0.25
LEFT = 0.25
THRESHOLD = 3

def get_slope(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((5, 5), dtype = np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    res = cv2.bitwise_and(frame, frame, mask= mask)
    coord = cv2.findNonZero(mask)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 2:
        left_contour = np.sum(contours[0], axis = 0)/len(contours[0])
        right_contour = np.sum(contours[1], axis = 0)/len(contours[1])
        
        cv2.circle(frame, (int(left_contour[0][0]), int(left_contour[0][1])), 32, (100, 100, 100), 5)
        cv2.circle(frame, (int(right_contour[0][0]), int(right_contour[0][1])), 32, (100, 100, 100), 5)
        print((int(left_contour[0][0]), int(left_contour[0][1])), (int(right_contour[0][0]), int(right_contour[0][1])))
        return (int(left_contour[0][0]), int(left_contour[0][1])), (int(right_contour[0][0]), int(right_contour[0][1]))
    
    else:
        raise ValueError("Length of contours is less than 0")

def backward(frame, lower_color, upper_color):
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, lower_color, upper_color)
    # kernel = np.ones((3, 3), dtype = np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # res = cv2.bitwise_and(frame, frame, mask= mask)
    # return np.sum(cv2.findNonZero(mask)) < THRESHOLD
    return False


if __name__ == "__main__":
    
    lower_red = np.array([155,25,0])
    upper_red = np.array([179,255,255])
    lower_blue= np.array([78,111,124])
    upper_blue = np.array([168,255,255])
    video = VideoStream(src=0).start()

    while(1):
        start_time = time.time()
        frame = video.read()
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        x1, y1, x2, y2 = 0, 0, 0, 0 
        try:
            (x1, y1), (x2, y2) = get_slope(frame, lower_blue, upper_blue)
            print(f"Time Taken for Slope Calculation: {time.time() - start_time}")
            cv2.imshow('frame',frame)
        
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        except ValueError:
            cv2.imshow('frame',frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        try:
            slope = (y2 - y1)/(x2 - x1)
            print(f"Slope: {slope}")
            if not backward(frame, lower_red, upper_red):
                if slope > RIGHT and slope < LEFT:
                    pyautogui.keyDown('w')
                    #time.sleep(0.002)
                    pyautogui.keyUp('w')
                elif slope > RIGHT and slope > LEFT:
                    pyautogui.keyDown('a')
                    pyautogui.keyDown('w')
                    #time.sleep(0.002)
                    pyautogui.keyUp('a')
                    pyautogui.keyUp('w')
                else:
                    pyautogui.keyDown('d')
                    pyautogui.keyDown('w')
                    #time.sleep(0.002)
                    pyautogui.keyUp('d')
                    pyautogui.keyUp('w')
            else:
                if slope > RIGHT and slope < LEFT:
                    pyautogui.keyDown('s')
                    #time.sleep(0.002)
                    pyautogui.keyUp('s')
                elif slope > RIGHT and slope > LEFT:
                    pyautogui.keyDown('d')
                    pyautogui.keyDown('s')
                    #time.sleep(0.002)
                    pyautogui.keyUp('d')
                    pyautogui.keyUp('s')
                else:
                    pyautogui.keyDown('a')
                    pyautogui.keyDown('s')
                    #time.sleep(0.002)
                    pyautogui.keyUp('a')
                    pyautogui.keyUp('s')
        except:
            pass
        
        print(f"Time taken for the entire algorithm: {time.time() - start_time}")
