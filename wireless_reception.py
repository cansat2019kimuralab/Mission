import serial
import sys
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import binascii
import codecs
import time
img_string=""
img_strings=[]
line=[]
cngtext=[]
count=0
print("a")
mybaudrate=57600

def setSerial(mybaudrate=57600):
    com=serial.Serial(
        port='COM7',
        baudrate=mybaudrate,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        timeout=None,
        xonxoff=False,
        rtscts=False,
        writeTimeout=None,
        dsrdtr=False,
        interCharTimeout=None)
    com.flushInput()
    com.flushOutput()
    return com

def Send(args, mybaudrate = 19200):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'TXDA' + binascii.b2a_hex(args.encode('utf-8')) + b'\r\n')
    com.readline()
    com.flushOutput()
    com.close()

with open('0806-2Log.txt', 'w') as f:
    print("b")
    #Send("1", 57600)
  #  with serial.Serial('COM7' ,57600, timeout=None) as ser:
    com=setSerial(mybaudrate)
    with com as ser:
     #while len(str(img_strings))<200000:
    #  while True:
      while 1:
        line = ser.readline().decode('utf-8')
        line=str(line)

        if line.find('65,6E,64') >-1:                    
            break
        else:
            head=line.find(":")
            data=line[head+1:head+203]
            data=data.replace(",","")
            count+=1
            print(count, data)

            img_strings.append(data)
            time.sleep(0.1)
            print("c")
            com.flushInput()
            com.write(b'TXDA' + binascii.b2a_hex(str(count).encode('utf-8')) + b'\r\n')
            com.readline()
            com.flushOutput()
            com.flushInput()
            com.write(b'TXDA' + binascii.b2a_hex(str(count).encode('utf-8')) + b'\r\n')
            com.readline()
            com.flushOutput()
            print("d")
      img_string=''.join(img_strings)#文字列にする
      print(len(img_string))
      img_string=img_string.replace(",","")
     # img_string=img_string.replace("\\r\\n","")#改行削除
     # img_string=img_string.replace("b'00,5A18,","")#b'00,5A18,削除

      
     # f.write(img_string)
      b = bytes.fromhex(img_string)
     # b=binascii.unhexlify(img_string)
  #   print(str(b))
      #b= binascii.a2b_hex(img_string)
      
      f.write(str(b))
      img_array = np.fromstring(b,dtype ='uint8') #バイトデータ→ndarray変換
     # img_array = np.reshape(img_array,(240,320))#エラーでた
             #   img_array=np.newaxis(img_array,(-1,-1))  #エラー出た
      img_array=np.resize(img_array,(240,320))
                         #dec_img = cv2.imdecode(img_array, 0)
      pil_img = Image.fromarray(img_array)
      
                        #cv2.imshow("decoded_image", dec_img)
                        #pil_img.show()
      print("end")
      pil_img.save("decoded_target0806-9.jpg")
      
      print("e")
      print(len(b))
      print("count"+str(count))
               # text=line.replace('\r\n','')
                #print(text)









