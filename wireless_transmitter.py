import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
import time
import difflib
import pigpio
import serial
import binascii
import IM920
import convertIMG2BYTES
import cv2
from PIL import Image
import traceback
'''
pi=pigpio.pi()
pi.set_mode(22,pigpio.OUTPUT)
pi.write(22,0)
time.sleep(1)
pi.write(22,0)
'''

count = 0
x=0
amari=0

t_start = 0


def selectphoto(photoPath,readmode):
	
	img = Image.open('/home/pi/git/kimuralab/Mission/photo5.jpg')
	img_resize = img.resize((160, 120))
	img_resize.save('/home/pi/git/kimuralab/Mission/sendPhoto.jpg')
	img=cv2.imread(photoPath,readmode)
	byte = convertIMG2BYTES.IMGtoBYTES(img)
	mode = 1
	return byte,mode

def transmitdata():
	for i in range(3):
		IM920.Send("M")
		IM920.Send("M")
		ack = str(IM920.read())
		comData = ack.rsplit(":", 1)
		ack = comData[1:]
		if(ack == ['4D']):
			mode = 0
		else:
			mode = 1
			break
		print(mode)
		time.sleep(0.5)
	print(mode)
	time.sleep(4)	
	return mode

def sendphoto(byte):
	with open("soushinlog.txt","w")as f:
		f.write(str(byte))
	for i in range(0,len(byte),64):
		data = IM920.IMSend(byte[i:i+64])
		cng = IM920.Reception()
		if(cng == ""):
			data = IM920.IMSend(byte[i:i+64])
			cng = IM920.Reception()
		time.sleep(0.1)
		count+=1
		print(count)

		#print(i,'/',len(byte))
		amari=len(byte)-i

	amari=len(byte)-i
	IM920.IMSend(byte[i:i+amari])
	#print(amari,'/',64)
	#print(str(byte[i:i+amari]))

	IM920.Send("end")
	time.sleep(1)
	IM920.Send("end")
	time.sleep(1)
	IM920.Send("end")

if __name__ == "__main__":
    try:
        mode=1
        photopath="/home/pi/git/kimuralab/Mission/sendPhoto.jpg"
        readmode=0
        byte,mode=selectphoto(photopath,readmode)
        print("link establish")

        while mode:
            mode=transmitdata()
        print("transmit start")

        t_start = time.time()

        sendphoto(byte)
        print(time.time() - t_start)

    except:
         print(traceback.format_exc())

