# calcOpticalFlowPyrLK 추적 (track_opticalLK.py)

import collections
import cv2
import numpy as np
import time
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

buffer = collections.deque(maxlen=140)

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('jump.mp4')

def press_space():
    keyboard.press(Key.space)
    keyboard.release(Key.space)


fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)
print(fps)
print(delay)
color = np.random.randint(0, 255, (200, 3))

lines = None
prevImg = None

termcriteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)

jumpcnt = 1        
cnt = 0
prevPt = None

for i in range (200):
    ret, frame = cap.read()
    scale_percent = 50  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('', gray)
    print(i)
    key = cv2.waitKey(delay)
cv2.destroyAllWindows()

while True:
    ret, frame = cap.read()

    scale_percent = 10  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    if not ret:
        break
    img_draw = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prevImg is None:
        prevImg = gray
        lines = np.zeros_like(frame)
        prevPt = cv2.goodFeaturesToTrack(prevImg, 200, 0.01, 10)
    else:

        nextImg = gray
        prevPt = cv2.goodFeaturesToTrack(prevImg, 200, 0.01, 10)

        nextPt, status, err = cv2.calcOpticalFlowPyrLK(prevImg, nextImg, \
                                                       prevPt, None, criteria=termcriteria)
        try:
            prevMv = prevPt[status == 1]
            nextMv = nextPt[status == 1]
            vec = prevMv - nextMv

            buffer.append(vec[1])
            Threshold = 0

            if len(buffer) > 40:
                Threshold = np.mean(np.array(buffer))

            vec = np.mean(vec, axis=0)
              

            if vec[1] > (Threshold+0.3 ) * (1/jumpcnt):
                #print(vec[1])  
                jumpcnt += 1
            else:
                jumpcnt = np.clip(jumpcnt - 1, 1, 5)
            if jumpcnt > 3:
                print('jump')
                jumpcnt = 1
                press_space()

            '''
            for i, (p, n) in enumerate(zip(prevMv, nextMv)):
                px, py = p.ravel()
                nx, ny = n.ravel()

                cv2.line(lines, (px, py), (nx, ny), color[i].tolist(), 2)

                cv2.circle(img_draw, (nx, ny), 2, color[i].tolist(), -1)

            img_draw = cv2.add(img_draw, lines)
            '''

            prevImg = nextImg
            prevPt = nextMv.reshape(-1, 1, 2)
        except:
            pass
   
    key = cv2.waitKey(delay)
    if key == 27:  # Esc:
        break
    elif key == 8:  # Backspace:
        prevImg = None

    cnt += 1
cv2.destroyAllWindows()
cap.release()

