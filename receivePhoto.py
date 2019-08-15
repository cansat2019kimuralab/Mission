import cv2
import time
import numpy as np

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

if __name__ == "__main__":
    while 1:
        print(read())