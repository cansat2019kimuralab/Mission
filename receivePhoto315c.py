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
import datetime
baudrate=19200
receptionLog=r"C:\Users\hp731\Documents\GitHub\Mission\315ccommunicationDecryptionLog.txt"
def setSerial(mybaudrate=19200):
    com=serial.Serial(
        port='COM8',
        baudrate=mybaudrate,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        timeout=3,
        xonxoff=False,
        rtscts=False,
        writeTimeout=None,
        dsrdtr=False,
        interCharTimeout=None)
    com.flushInput()
    com.flushOutput()
    return com

com=setSerial(19200)    

def Reception(mybaudrate =19200):
    global com
    '''

    受信
    アスキーコードから文字列に変換したものを返す
    mybaudrate:ボーレート
    '''
    try:
        com.flushInput()
        #print("a")
        text = com.readline().decode('utf-8').strip() #受信と空白の削除
        #print(text)
        com.flushOutput()
        text = text.replace("\r\n","")
        #power=text.split(":")[0]
        #print(text)
        text = text.split(":")[1]
        #print(text)
        text = text.split(",")
        #print("d")
        cngtext = ""
        #print(text)
        for x in text:
            cngtext += chr(int(x,16))
            Other.saveLog(receptionLog,  cngtext, datetime.datetime.now())
        #f.write(text)
        #f.write("\n")
        #print(text)
        
    except Exception:
        cngtext = ""
        print("NO DATA")
    #com.close()
    return cngtext
    
    



array=[[[0]*3]*80]*60
array=np.zeros_like(array)
I=list(range(5))


if __name__ == "__main__":
    try: 
        while 1:
            re = Reception(19200)
            
            if re == "":
                
                continue
            if re[0] == 'P':                 
                print("phase")
                print(re)
                continue
            if re[0] == 'M':      #MissionFinish          
                print(str(re))    
                break
            if re[0]== 'G':
                print(str(re))
                continue
            if re[0]== 'E':
                print(str(re))
                continue
            #print(len(re))
            
            b=re[-3:]
            g=re[-6:-3]
            r=re[-9:-6]
            j=re[-12:-9]
            i=re[:-12]
            if i == '':
                i = 0
            
            if j == '':
                j = 0


            print(i, j, r, g, b)

            B = int(b)
            G = int(g)
            R = int(r)
            I = int(i)
            J = int(j)
            
            '''
            if len(re)==13:
                i=re[-13:-12]
            elif len(re)==14:
                i=re[-14:-13]
            elif len(re)==15:
                i=re[-15:-14]
            '''
            
            #print(re, re[-6:-3], re[-3:])
            array[I][J][0]=R
            array[I][J][1]=G
            array[I][J][2]=B
            
            #time.sleep(0.02)
    
        cv2.imwrite('receive315c.jpg',array)

        np.save('sample_315c.npy', array)
    except :
        com.close()
        print(traceback.format_exc())