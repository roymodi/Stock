import cv2
# pip install opencv-python  

#camp = 'http://192.168.43.1:4747/video'
camp = "http://192.168.137.144:4747/video"
cap=cv2.VideoCapture(camp)
while True:
    ret,frame = cap.read()
    cv2.imshow('Capturing',frame)
    with open ('video.mp4','ab')as op:
        op.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()



"""
thisi is faceid identyfy using facecamp
import cv2
import sys

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
camp = "http://192.168.137.144:4747/video"
#camp = 'http://192.168.43.1:4747/video'
cap=cv2.VideoCapture(camp)

while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,225,0),2)

    cv2.imshow('Capturing',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

"""