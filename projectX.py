import serial
import numpy as np
import cv2
from PIL import Image
img_string=""
img_strings=[]
line=[]
cngtext=[]

print("a")

with open('Log.txt', 'w') as f:
    print("b")
    with serial.Serial('COM7' ,19200, timeout=None) as ser:

     #while len(str(img_strings))<200000:
    #  while True:
      while 1:
          
       # if '5A18' in line:
            #    print("c")
              #  line = ser.readline()#.decode('utf-8')
                #line=str(line)
                line = ser.readline().decode('utf-8')
               # print(line)

                if line.find('65,6E,64') >-1:
                    print("end")
                    break
               
                else:
                     #print("c")
                     #print(line)
                     head=line.find(":")
                     data=line[head+1:head+205]
                     print(data)
                     data=data.replace("\\r\\n","")
                    # data=data.replace(",","")
                    # print("d"+data) 
           
                    #    f.write(line)
                
                     img_strings.append(data)
                     print(len(str(img_strings))) 
                      #  img_string=''".join(img_strings)
      #  else:
      print("a")
      img_string=''.join(img_strings)#文字列にする
      img_string=img_string.replace(",","")
     # img_string=img_string.replace("\\r\\n","")#改行削除
     # img_string=img_string.replace("b'00,5A18,","")#b'00,5A18,削除

      print(img_string)
     # f.write(img_string)
      b = bytes.fromhex(img_string)
      
     
      f.write(str(b))
      img_array = np.fromstring(b,dtype ='uint8') #バイトデータ→ndarray変換
      #img_array = np.reshape(img_array,(240,320))#エラーでた
             #   img_array=np.newaxis(img_array,(-1,-1))  #エラー出た
      img_array=np.resize(img_array,(240,320))
                         #dec_img = cv2.imdecode(img_array, 0)
      pil_img = Image.fromarray(img_array)
      
                        #cv2.imshow("decoded_image", dec_img)
                        #pil_img.show()
      print("d")
      pil_img.save("decoded_target18.jpg")
      print("e")
            
               # text=line.replace('\r\n','')
                #print(text)








