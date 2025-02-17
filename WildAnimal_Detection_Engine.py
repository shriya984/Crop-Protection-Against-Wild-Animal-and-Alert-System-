import numpy as np
import cv2
import os
import cv2
import sys
import glob
import random
import importlib.util
from tensorflow.lite.python.interpreter import Interpreter
import operator
import collections
import matplotlib   



import matplotlib.pyplot as plt
from mutagen.mp3 import MP3
from gtts import gTTS
import pyglet
import os, time
import threading
import WhatsAppSender
modelpath="model/detect.tflite"
lblpath='model/labelmap.txt'
min_conf=0.5
txt_only=False




def playvoice(playtext):
    #fetch project name
   tts = gTTS(text=playtext, lang='en')
   ttsname=("voice.mp3")
   
   tts.save(ttsname)
   audio = MP3("voice.mp3")
   val= audio.info.length
  
   x=int(val)+1
   print(" audio length",x)
   music = pyglet.media.load(ttsname, streaming = False)
   music.play()
   os.remove(ttsname)
   time.sleep(x)
   
with open(lblpath, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Load the Tensorflow Lite model into memory
interpreter = Interpreter(model_path=modelpath)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

float_input = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5      
    
      
cap=cv2.VideoCapture(1)
count=0
xmin=1
xmax=250
current,previous=0,0
shootlist=[]
animal_name=""
while cap.isOpened():
    _,capimg=cap.read()
    cv2.imwrite("temp.jpg", capimg)
    image_rgb = cv2.cvtColor(capimg, cv2.COLOR_BGR2RGB)
    imH, imW, _ = capimg.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[1]['index'])[0] # Bounding box coordinates of detected objects #about inedx points
    classes = interpreter.get_tensor(output_details[3]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[0]['index'])[0] # Confidence of detected objects

    detections = []
    for i in range(len(scores)):
        if ((scores[i] > min_conf) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
           # current=xmin
           # print("C : ",current)
            
            

            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            finscore=int(scores[i]*100)
            if(finscore>=99):
                cv2.rectangle(capimg, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                animal_name= object_name              
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(capimg, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255,255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(capimg, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
    
                detections.append([object_name, scores[i], xmin, ymin, xmax, ymax])
            
                
                if(count==0):
                    
                    
                    current=xmin
                    previous=xmin
                    print("C : ",current," : P ",previous)
                    count=count+1
                else:
                   
                    current=xmin
                   
                   # print("C : ",current," : P ",previous)
                    diff=abs(current-previous)
                    if(diff<5=):
                        shootvalue="in_range"
                        shootlist.append(shootvalue)
                        fincount=len(shootlist)
                        previous=current
                        print("Fincount ",fincount)
                        if(fincount>=30):
                            print("Shooting now")
                            shootlist.clear()
                           
                            text="WILD ANIMAL IS DETECTED"
                            t1 = threading.Thread(target=playvoice, args=(text,))
                            t1.start()
                            
                            import ServoShooter
                            ServoShooter.shootinit()
                            newimage = cv2.imread('temp.jpg')
                            newfilename="temp_waIMG.jpg"
                            cv2.imwrite(newfilename, newimage)
                            WhatsAppSender.sendInfoWA(newfilename,animal_name)
                            
                            break
                            
                        
                    else:
                        shootlist.clear()
                        previous=current
                         
    
    cv2.imshow('Capture Image( Press q to quit)',capimg)
    
    if cv2.waitKey(1)==ord('q'):
        break
       
      
                
          


cap.release()
cv2.destroyAllWindows()