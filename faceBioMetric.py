import os
import face_recognition as fc
import pandas as pd
import cv2
import time
import numpy as np
import calendar
import datetime
import smtplib
nameList=[]
encList=[]


def createReport():
   monthNam=input('Enter month Name(First Three Charactors)-')
   monthNameCap=monthNam.capitalize()
   allMonth={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
   
   emailList=['manish.cse17@hotmail.com','manish.cse17@hotmail.com','manish.cse17@hotmail.com','manish.cse17@hotmail.com']   
   s=smtplib.SMTP('smtp.gmail.com',587)
   s.starttls()
   f=open('/home/manish/Desktop/College/pswrd.txt','r')
   pswrd=f.read()
   s.login('manish10meena@gmail.com',pswrd)
   print('Logged In')

   df=pd.read_csv('attend.csv')
   colName=list(df.columns[1:])
   colDate=list(df['Dates'])

   now=datetime.datetime.now()
   monthNum=allMonth[monthNameCap]
   monthDays=calendar.monthrange(now.year,monthNum)[1]

   countList=[]
   for i in range(0,len(colName)):
       countList.append(0)
       
   for i in colName:
       for j in colDate:
           if(monthNameCap in j):
               if(df[i][colDate.index(j)]==1):
                   countList[colName.index(i)]=countList[colName.index(i)]+1

   print(countList)

   for i in range(0,len(colName)):
       percentAtt=(countList[i]/monthDays)*100
       message='Your Son/Daughter-'+ (colName[i].split('.')[0]).capitalize() +' have atteneded-'+str(percentAtt)+'% Classes in '+monthNameCap+'-'+str(now.year)
       s.sendmail('manish10meena@gmail.com',emailList[i],message)
       print('Sent-',i+1)

   print('Mailed all report to thier Mail Id')
   s.quit()
      
def markAttend(pm):
   dateList=time.ctime().split(' ')
   currentDate=str(dateList[1])+'-'+str(dateList[2])+'-'+str(dateList[4])

   df=pd.read_csv('attend.csv')
   da=df.values
   dfHead=['Dates']
   for i in nameList:
      dfHead.append(str(i))
   arrayDate=da[:,0]

   if(currentDate not in arrayDate):
      appendRow=[]
      for i in range(0,len(dfHead)):
         if(i==0):
            appendRow.append(currentDate)
         else:
            appendRow.append(0)
      da=np.append(da,[appendRow],axis=0)
      
   arrayDate=da[:,0]

   #print('Value',da[list(arrayDate).index(currentDate),dfHead.index(pm)])
   da[list(arrayDate).index(currentDate),dfHead.index(pm)]=1
   
   saveDf=pd.DataFrame(da,columns=dfHead)
   saveDf.to_csv('attend.csv',index=False)

   print('Attendence Done of-',(pm.split('.')[0]).capitalize())

         
def captureFace():
    print('Please Put your face in front of Camera...')
    print('Capturing...')
    v=cv2.VideoCapture(0)
    while True:
        r,live=v.read()
        i=cv2.resize(live,(500,500))
        fl=fc.face_locations(live)
        print(fl)
        if(len(fl)>0):
            [x1,y1,x2,y2]=fl[0]
            cv2.rectangle(live,(y2,x1),(y1,x2),(0,0,255),5)
            enc=fc.face_encodings(live,fl)[0]
            res=fc.compare_faces(encList,enc)
            resf=True in res
            if(resf==True):
                nameInd=res.index(True)
                pm=nameList[res.index(True)]
                print(pm)
                
        cv2.imshow('Camera',live)
        k=cv2.waitKey(5)
        if(k==ord('c')):
            print('Captured')
            time.sleep(2)
            cv2.destroyAllWindows()
            v.release()
            markAttend(pm)
            break    
        
def saveDataBase():
   df=pd.DataFrame({'Names':nameList,'Encoding Of Name':encList})
   df.to_csv('encodings.csv',index=False)

def FaceEnc(cwd,cwp):
    print('\n')
    print(cwd)
    print(cwp)

    a=fc.load_image_file(cwd+'/'+cwp)
    fl=fc.face_locations(a)
    e=fc.face_encodings(a,fl)
    print(fl)
    print(len(fl))

    var=0
    for i in range(0,len(fl)):
        nameList.append(cwp+str(var))
        encList.append(e[var])
        var=var+1

def workingDir():
    listDir=os.listdir(os.getcwd())
    #print(listDir)
    os.chdir(os.getcwd()+'/'+listDir[listDir.index('Photos')])
    #print(os.getcwd())
    listDir=os.listdir(os.getcwd())
    mainWD=os.getcwd()
    print('Main Dir-'+mainWD)
    print('Folders',listDir)
        
    for pdn in listDir:
        pwd=os.chdir(mainWD+'/'+pdn)
        photos=os.listdir(pwd)
        
        for cwp in photos:
            cwd=os.getcwd()
            FaceEnc(cwd,cwp)
    os.chdir('/home/manish/Desktop/ML/Projects/FaceEncodings')
    print(os.getcwd())
    saveDataBase()
     
def viewTime():
    timeList=time.ctime().split(' ')
    print('\t\t      Time-'+timeList[3])
    return timeList[3]
   
workingDir()

print(nameList)
print('\t \t    Bio Metric Security')

while True:
    print('--------------------------------------------------------------')
    print('------------------ Welcome To BMS System ---------------------')
    retTime=viewTime()
    userInput=int(input('1.Attendence \n2.Report \n3.Exit \nEnter the Choice-'))
    mMod=int(retTime[3:5])%60
    hMod=int(retTime[:2])%24
    if(userInput==1):
       if(int(hMod==7)):
          if(mMod in range(0,60)):
             captureFace()
          else:
             print('Your are late...')
       else:
          print('Your are late')
    elif(userInput==2):
       createReport()
    elif(userInput==3):
        break
