import cv2
import os

datasetpath="Wild Animal Dataset"


if not os.path.exists(datasetpath):
    os.makedirs(datasetpath)   

    
      
cap=cv2.VideoCapture(0)
imgeno=1

while cap.isOpened():
    _,capimg=cap.read()
  
      
   
    cv2.imshow('Wil Animal Dataset Creator Image( Press q to quit)',capimg)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
    # SPACE pressed
        filename=str(imgeno)   
        newfilepath=datasetpath+"//"+filename+".jpg" # Wild Animal Dataset//1.jpg
     
        cv2.imwrite(newfilepath,capimg)
        imgeno=imgeno+1
        print("Image path is ",newfilepath)
      
                
          


cap.release()
cv2.destroyAllWindows()