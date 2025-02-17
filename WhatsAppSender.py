import pywhatkit as pwk
import datetime


def sendInfoWA(newfilename,animal_name):
   
   
    lat=" 18.061300"
    longi="73.786902"
    urlstr="https://www.google.com/maps/dir/"+lat+","+longi
    message="ALERT ALERT ALERT !!! \n An Animal "+animal_name+ "is captured by our survelliance camera in your field \n"
    message=message+urlstr+"\n ";
    message=message+". And also attached Surveilliance Image for your reference. PLEASE TAKE ACTION IMMMEDIATLY \n ";
    message=message+" Regards - \n Automatic wild animal Detection System"
    mobilenumber="+917820898751";
 
    reference_image_path=newfilename
    
   # WhatsAppSender.sendImage(mobilenumber, reference_image_path, message)
    datet=str(datetime.datetime.now())
    st=datet.split(" ")
    kt=st[1].split(":")
    hourstr=kt[0]
    minstr=kt[1]
    hr=int(hourstr)
    min=int(minstr)
    if(min<59):
        min=min+1
    else:
        min=1
        hr=hr+1
    print(hr)
    print(min)
    
   
    pwk.sendwhats_image(mobilenumber, reference_image_path,message)
    
 
if __name__ == '__main__':
    sendInfoWA()
 
    