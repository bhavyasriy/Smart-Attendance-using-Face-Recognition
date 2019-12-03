"""
Authors: Bhavana,Keerthana,Bhavya,Sravani
"""

import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

window = tk.Tk()
window.title("Smart Logbook")

dialog_title = 'EXIT'
dialog_text = 'Do you want to quit really?'
 
#window.geometry('1280x720')
window.configure(background='black')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)



message = tk.Label(window, text="Smart Logbook" ,bg="gray"  ,fg="black"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

message.place(x=200, y=20)

lbl = tk.Label(window, text="ID",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20  ,bg="yellow" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Name",width=20  ,fg="red"  ,bg="yellow"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20  ,bg="yellow"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)

lbl3 = tk.Label(window, text="Status : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold underline ')) 
lbl3.place(x=400, y=400)

message = tk.Label(window, text="" ,bg="yellow"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=700, y=400)

lbl3 = tk.Label(window, text="Report : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold  underline')) 
lbl3.place(x=400, y=650)


message2 = tk.Label(window, text="" ,fg="red"   ,bg="yellow",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=700, y=650)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
	Id=(txt.get())
	name=(txt2.get())
	if(is_number(Id) and name.isalpha()):
		cam = cv2.VideoCapture(0)
		harcascadePath = "haarcascade_frontalface_default.xml"
		detector=cv2.CascadeClassifier(harcascadePath)
		sampleNum=0
		while(True):
			ret, img = cam.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			faces = detector.detectMultiScale(gray, 1.3, 5)
			for (x,y,w,h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
				#incrementing sample number 
				sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
				cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
				cv2.imshow('frame',img)
            #wait for 100 miliseconds 
			if cv2.waitKey(100) & 0xFF == ord('q'):
				break
            # break if the sample number is morethan 100
			elif sampleNum>60:
				break
		cam.release()
		cv2.destroyAllWindows()
		res = "Images Saved for your Id : " + Id +" Name : "+ name
		"""ts = time.time()      
		date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')"""
		row = [Id , name]
		with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(row)
		csvFile.close()
		message.configure(text= res)
	else:
		if(is_number(Id)):
			res = "Enter Alphabetical Name"
			message.configure(text= res)
		if(name.isalpha()):
			res = "Enter Numeric Id"
			message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empty face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
	recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
	recognizer.read("TrainingImageLabel\Trainner.yml")
	harcascadePath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(harcascadePath);    
	df=pd.read_csv("StudentDetails\StudentDetails.csv")
	cam = cv2.VideoCapture(0)
	font = cv2.FONT_HERSHEY_SIMPLEX        
	col_names =  ['Id','Name','Date','Time','Present']
	attendance = pd.DataFrame(columns = col_names)    
	while True:
		ret, im =cam.read()
		gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		faces=faceCascade.detectMultiScale(gray, 1.2,5)    
		for(x,y,w,h) in faces:
			cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
			Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
			if(conf < 50):
				ts = time.time()      
				date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
				timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
				aa=df.loc[df['Id'] == Id]['Name'].values
				
				timeStamp2='24:00:00'
				s1,s2='Yes','No'
				if(timeStamp>timeStamp2):
					s3=s2
				else:
					s3=s1
				#ho=timeStamp.hour
				#ho=attendance.timeStamp.dt.hour
				#attendance['Hours']=attendance['timeStamp'].dt.hour
				tt=str(Id)+"-"+aa
				attendance.loc[len(attendance)] = [Id,aa,date,timeStamp,s3]
				"""row = [Id , aa ,date , timeStamp]
				with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
					writer = csv.writer(csvFile)
					writer.writerow(row)
				csvFile.close()"""
			else:
				Id='Unknown'                
				tt=str(Id)  
			if(conf > 75):
				noOfFile=len(os.listdir("ImagesUnknown"))+1
				cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
			cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
		attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
		cv2.imshow('im',im) 
		if (cv2.waitKey(1)==ord('q')):
			break
	ts = time.time()      
	date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
	timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
	Hour,Minute,Second=timeStamp.split(":")
	with open('Attendance\Attendance_'+date+'.csv','a+') as temp:
		fileName=temp
		attendance.to_csv(fileName,index=False)
	cam.release()
	cv2.destroyAllWindows()
    #print(attendance)
	res=attendance
	message2.configure(text= res)   
	fromaddr = "sender@gmail.com"
	toaddr = "receiver@gmail.com"
   
# instance of MIMEMultipart 
	msg = MIMEMultipart() 
  
# storing the senders email address   
	msg['From'] = fromaddr 
  
# storing the receivers email address  
	msg['To'] = toaddr 
  
# storing the subject  
	msg['Subject'] = "Smtp send csv"
  
# string to store the body of the mail 
	body = "trial"
  
# attach the body with the msg instance 
	msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
	filename = "Attendance"
	attachment = open('Attendance\Attendance_'+date+'.csv', "rb") 
	#attachment = open('StudentDetails\StudentDetails.csv', "rb") 

# instance of MIMEBase and named as p 
	p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
	p.set_payload((attachment).read()) 
  
# encode into base64 
	encoders.encode_base64(p) 
   
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
	msg.attach(p) 
  
# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587)
#s=smtplib.SMTP('smtp,googlemail.com',465) 
  
# start TLS for security 
	s.starttls() 
  
# Authentication 
	s.login(fromaddr, "sender_password") 
  
# Converts the Multipart msg into a string 
	text = msg.as_string() 
  
# sending the mail 
	s.sendmail(fromaddr, toaddr, text) 
  
# terminating the session 
	s.quit() 
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Detect Images", command=TrackImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=800, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=500)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.insert("insert", "Developed by Team SB2K","")
copyWrite.configure(state="disabled",fg="white"  )
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)
 
window.mainloop()
