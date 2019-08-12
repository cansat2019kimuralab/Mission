import sys
import binascii
import codecs
import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
import traceback
import warnings
from PIL import Image
from matplotlib import pyplot as plt
import Other
warnings.simplefilter("ignore", DeprecationWarning) #Ignore Warning of DeprecationWaring

img_string=""
img_strings=[]
line=[]
cngtext=[]
receptionLog=r"C:\Users\hp731\Documents\GitHub\Mission\communicationDecryptioLogLog.txt"
baudrate=57600
num=[0,0,0] 
power=0 #valiable for receive strenghth
comdata=[] #valiable for receive phase
def setSerial(mybaudrate=57600):
    com=serial.Serial(
        port='COM7',
        baudrate=mybaudrate,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        timeout=5,
        xonxoff=False,
        rtscts=False,
        writeTimeout=None,
        dsrdtr=False,
        interCharTimeout=None)
    com.flushInput()
    com.flushOutput()
    return com

def Send(args, mybaudrate = 57600):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'TXDA' + binascii.b2a_hex(args.encode('utf-8')) + b'\r\n')
    com.readline()
    com.flushOutput()
    com.close()

def read(mybaudrate = 57600):
  re = ""
  try:
    com = setSerial(mybaudrate)
    com.flushInput()
    re = str(com.readline().decode('utf-8').strip())
    com.flushOutput()
    print(str(re))
  except Exception:
    re = ""
    #print("no data")
  return re

def getCommand(im920data):
  try:
   comData = im920data.rsplit(":", 1)
   num=comData[0].split(",")
   power=num[2]
   print(num[2])
   return comData[1:],power
  except Exception:
   a=0
   b=0
   return a,b

def receivePhoto(logPath, photoPath,photoSize, convertedPhotoSize):
  count = 0
  # --- Receive Photo from IM920 --- #
  com = setSerial(baudrate)
  with com as ser:
    while 1:
      line = ser.readline().decode('utf-8')
      line=str(line)

      if line.find('4D,46,65,6E,64') >-1:      #MissionFinish              
        break
      else:
        head=line.find(":")
        data=line[head+1:head+203]
        data=data.replace(",","")
        count+=1
        print(count)

      img_strings.append(data)
      #time.sleep(0.05)

      for i in range(3):
        com.flushInput()
        com.write(b'TXDA' + binascii.b2a_hex(str(count).encode('utf-8')) + b'\r\n')
        com.readline()
        com.flushOutput()

  # --- Convert to String --- #
  img_string=''.join(img_strings)
  #print(len(img_string))
  img_string=img_string.replace(",","")
  b = bytes.fromhex(img_string)

  # --- Save Log --- #
  with open(logPath, 'w') as f:
    f.write(str(b))

  # --- Convert to Photo --- #
  img_array = np.fromstring(b, dtype ='uint8')  #Convert from byte to array
  img_array = np.resize(img_array, photoSize)   #Resize array
  pil_img = Image.fromarray(img_array)          
  pil_img.save(photoPath + "-1.jpg")            #Save Photo

  pil_img = pil_img.resize(convertedPhotoSize)  #Convert to QVGA
  pil_img.save(photoPath + "-2.jpg")            #Save QVGA
  #print(len(b))
  #print("count "+str(count))

def powerread(power):
  power=str(power)
  power = int(power, 16)
  print(power)
  print("strength: "+str(power))

def receiveData(data):
  returnVal = 0
  #print(data)
  comdata,power= getCommand(data)

  if(comdata==['91']):
      Other.saveLog(receptionLog, "1-1", "Program Started", power, time.time())
      returnVal=2
      powerread(power)
      print("Program Started")

  elif(comdata==['50,31,46']):
      Other.saveLog(receptionLog, "1-2", "Program Started", power, time.time())
      returnVal=2
      powerread(power)
      print("Program Started2")

  elif(comdata==['50,32,53']):
      Other.saveLog(receptionLog, "2", "Sleep Started", power, time.time())
      returnVal=2
      powerread(power)
      print("Sleep Started")

  elif(comdata==['50,32,44']):
      Other.saveLog(receptionLog, "2", "Sleep now", power, time.time())
      returnVal=2
      powerread(power)
      print("Sleep Now")

  elif(comdata==['50,32,46']):
      Other.saveLog(receptionLog, "2", "Sleep Finished", power, time.time())
      returnVal=2
      powerread(power)
      print("Sleep Finished")

  elif(comdata==['50,33,53']):
      Other.saveLog(receptionLog, "3", "Release started", power, time.time())
      returnVal=2
      powerread(power)
      print("Release Started")

  elif(comdata==['50,33,44']):
      Other.saveLog(receptionLog, "3", "Release judge now", power, time.time())
      returnVal=2
      powerread(power)
      print("Release judge now")

  elif(comdata==['50,33,46']):
      Other.saveLog(receptionLog, "3", "Release judge finished", power, time.time())
      returnVal=2
      powerread(power)
      print("Release judge finished")

  elif(comdata==['50,34,53']):
      Other.saveLog(receptionLog, "4", "Land started", power, time.time())
      returnVal=2	
      powerread(power)
      print("Land judge started")

  elif(comdata==['50,34,44']):
      Other.saveLog(receptionLog, "4", "Land judge now", power, time.time())
      returnVal=2
      powerread(power)
      print("Land judge now")

  elif(comdata==['50,34,46']):
      Other.saveLog(receptionLog, "4", "Land FInished", power, time.time())
      returnVal=2
      powerread(power)
      print("Land judge finished")


  elif(comdata==['50,35,53']):
      Other.saveLog(receptionLog, "5", "Melt started", power, time.time())
      returnVal=2
      powerread(power)
      print("Melt Started")

  elif(comdata==['50,35,46']):
      Other.saveLog(receptionLog, "5", "Melt Finished", power, time.time())
      returnVal=2
      powerread(power)
      print("Melt finished")

  elif(comdata==['50,36,53']):
      Other.saveLog(receptionLog, "6", "ParaAvoidance started", power, time.time())
      returnVal=2	 
      powerread(power)
      print("ParaAvoidance started")  
    
  elif(comdata==['50,36,46']):
      Other.saveLog(receptionLog, "6", "ParaAvoidance finished", power, time.time())
      returnVal=2
      powerread(power)
      print("ParaAvoidance finished")

  elif(comdata==['50,37,53']):
      Other.saveLog(receptionLog, "7", "Running Phase Started", power, time.time())
      returnVal=2
      powerread(power)
      print("Running Phase Started")

  elif(comdata==['50,37,46']):
      Other.saveLog(receptionLog, "7", "Running Phase Finished", power, time.time())
      returnVal=2
      powerread(power)
      print("Running Phase Finished")

  elif(comdata==['50,38,53']):
      Other.saveLog(receptionLog, "8", "GoalDetection Phase Started", power, time.time())
      returnVal=2
      powerread(power)
      print("GoalDeetection Phase Started")

  elif(comdata==['50,38,46']):
       Other.saveLog(receptionLog, "8", "Running Phase Finished", power, time.time())
       returnVal=2
       powerread(power)
       print("Running Phase Finished")

  elif str('47') in str(comdata):	#GPS
      gps = int(comdata, 16)
      print(gps)
      Other.saveLog(receptionLog, "0", "GPS", gps, power, time.time())

  elif(comdata == ['4D']):
    for i in range(3):
      if(comdata == ['4D']):
        Send("M", baudrate)
        Send("M", baudrate)
        #print(data)
        time.sleep(0.1)
        data = read(baudrate)
        data = getCommand(data)
        time.sleep(0.2)
        returnVal = 1
      else:
        returnVal = 0
        break
  else:
    returnVal = 0

  print(data,power)
  return returnVal


if __name__ == "__main__":
  try:
    mode = 0
    logPath = "photoRecieveLog.txt"
    photoPath = "receivePhoto"
    photoSize = (120, 160)
    convertedPhotoSize = (320, 240)
    Other.saveLog(receptionLog, "0", "program start", time.time())
    print("Ready")
    while 1:
      im920data = read(baudrate)
      mode = receiveData(im920data)
      if(mode == 1):
        t_start=time.time()
        print("Photo Receive")
        receivePhoto(logPath, photoPath, photoSize, convertedPhotoSize)
        print(time.time()-t_start)
        print("MissionFinish")
        
      else:
        print("mode : "+str(mode))
  
    
  except IndexError:
    print(traceback.format_exc())

  except :
      print(traceback.format_exc())