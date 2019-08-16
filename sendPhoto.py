import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
import cv2
import time
import numpy as np

import IM920

img = cv2.imread("/home/pi/photo/photo21.jpg")
img = cv2.resize(img, (160, 120))
cv2.imwrite('sendPhoto.jpg', img)

num = 1000000
IM920.Send(str(num))
print(num)


print("Start")

'''
for i in range(len(img)):
	for j in range(len(img[i])):
		num = int(img[i][j][0]) + j * 1000 + i * 1000000
		IM920.Send(str(num))
		print(num, i, j, img[i][j][0])
		#time.sleep(0.05)
	#print(i)
'''

print("Finish")
