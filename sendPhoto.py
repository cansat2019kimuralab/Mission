import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/Other')
import cv2
import numpy as np
import os
import time

import IM920
import Other

sendPhotoPath = '/home/pi/photo/sendPhoto'
sendPhotoName = ''

def sendPhoto(photoPath):
	returnVal = 0
	if os.path.exists(photoPath):
		img = cv2.imread(photoPath)
		img = cv2.resize(img, (80, 60))
		#sendPhotoName = Other.fileName(sendPhotoPath, 'jpg')
		#cv2.imwrite(sendPhotoName, img)

		#print("Start")
		t = time.time()
		count = 0
		for i in range(len(img)):
			for j in range(len(img[i])):
				num = int(img[i][j][2]) + int(img[i][j][1]) * (10 ** 3) + int(img[i][j][0]) * (10 ** 6) + j * (10 ** 9) + i * (10 ** 12)
				sendStatus = IM920.Send(str(num))
				#print(sendStatus)
				t_send = time.time()
				while(sendStatus != b'OK\r\n'):
					if(time.time() - t_send > 3):
						break
					else:
						time.sleep(0.01)
						sendStatus = IM920.Send(str(num))
						#print("Send")
						count = count + 1
				print(num)
		print(count)
		time.sleep(0.1)
		IM920.Send("MF")
		time.sleep(0.1)
		IM920.Send("MF")
		time.sleep(0.1)
		IM920.Send("MF")
		print(time.time() - t)
		print("Finish")
		returnVal = 1
	else:
		print("File Not Found")
		returnVal = 0
	return returnVal

if __name__ == "__main__":
	photoName = "/home/pi/photo/photo21.jpg"
	sendPhotoStatus = sendPhoto(photoName)
	print(sendPhotoStatus)