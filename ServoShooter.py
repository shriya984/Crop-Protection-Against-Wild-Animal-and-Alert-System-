from pyfirmata import Arduino,SERVO,util
from time import sleep
x=1
port1="COM5"
pin1=8
board1=Arduino(port1)
board1.digital[pin1].mode=SERVO
 
 
 
port2="COM4" 

pin2=9
board2=Arduino(port2)
board2.digital[pin2].mode=SERVO

  
    
def shoot(pin2,angle):
    board2.digital[pin2].write(angle)
    sleep(0.00000001)
        
 
    
def rotateGUN(pin1,angle):
    board1.digital[pin1].write(angle)
    global x
    for i in range(0,180):
        if(x==1):
            shoot(pin2, i) 
            x=x+1
    sleep(0.000001)
        
    
def shootinit():
     
    for i in range(0,90):
        rotateGUN(pin1, i)    
        sleep(0.000001)  
#shoot()
#shootinit()
#shootinit()       
