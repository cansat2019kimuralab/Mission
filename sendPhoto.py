import sys
sys.path.append("home/pi/kimuralab/Mission")
import cv2
import time
import numpy as np

import IM920

img = cv2.imread("/home/pi/photo/photo21.jpg")
img = cv2.resize(img, (160, 120))
cv2.imwrite('sendPhoto.jpg', img)

for i in range(len(hide)):
    for j in range(len(hide[i])):
        IM920.Send(str(i) + ":" + str(j) + ":" + str(hide[i][j][0]) + ":" + str(hide[i][j][1] + ":" +  str(hide[i][j][2]))