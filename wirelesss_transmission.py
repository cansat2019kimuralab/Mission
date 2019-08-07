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
count=0
'''
pi=pigpio.pi()
pi.set_mode(22,pigpio.OUTPUT)
pi.write(22,0)
time.sleep(1)
pi.write(22,0)
'''
x=0
amari=0
img = cv2.imread("/home/pi/git/kimuralab/SensorModuleTest/Camera/photo80.jpg",0)
byte = convertIMG2BYTES.IMGtoBYTES(img)
with open("soushinlog.txt","w")as f:
	f.write(str(byte))
#print(byte[0:100])

for i in range(0,len(byte),64):
	#if i%640==0:
		#print("sleep")
		#time.sleep(0.5)
	if i==3840:
		time.sleep(3)
	data = IM920.IMSend(byte[i:i+64])
	cng = IM920.Reception()
	if(cng == ""):
		data = IM920.IMSend(byte[i:i+64])
		cng = IM920.Reception()
	time.sleep(0.1)
	count+=1
	print(count, data)

	print(i,'/',len(byte))
#	print(str(byte[i:i+63]))
	amari=len(byte)-i
#	print(str(amari))
amari=len(byte)-i
IM920.IMSend(byte[i:i+amari])
print(amari,'/',64)
print(str(byte[i:i+amari]))
IM920.Send("end")
time.sleep(1)
IM920.Send("end")
time.sleep(1)
IM920.Send("end")
'''
for i in range(0,len(byte)):
	IM920.IMSend(byte[i])
	print(i,'/',len(byte))


for i in range(0,len(byte),16):
	st = str(byte[i:i+15])
	IM920.Send(st)
	print(i,'/',len(byte))
'''
#IM920.IMSend(byte)
#convertIMG2BYTES.BYTEStoIMG(st)
