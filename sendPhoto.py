import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
import cv2
import time
import numpy as np

import IM920


def sendPhoto(photoPath):
	img = cv2.imread(photoPath)
	img = cv2.resize(img, (80, 60))
	cv2.imwrite('sendPhoto.jpg', img)

	#print("Start")
	t = time.time()
	for i in range(len(img)):
		for j in range(len(img[i])):
			num = int(img[i][j][2]) + int(img[i][j][1]) * (10 ** 3) + int(img[i][j][0]) * (10 ** 6) + j * (10 ** 9) + i * (10 ** 12)
			IM920.Send(str(num))
			print(num)
	IM920.Send("P1F")
	IM920.Send("P2S")
	IM920.Send("MF")
	IM920.Send("MF")
	IM920.Send("MF")
	print(time.time() - t)
	print("Finish")

if __name__ == "__main__":
	photoName = "/home/pi/photo/photo21.jpg"
	sendPhoto(photoName)
