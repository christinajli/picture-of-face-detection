import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

# read in image
img = cv2.imread(os.path.join("training_data", "wanda-face.jpeg"))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# detect faces
frontal_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# set minNeighbor to high to avoid false positives since by assumption, only one face per image
faces = frontal_face_cascade.detectMultiScale(gray, 1.2, 10)

face_imgs = list()
if len(faces)!=0: 
    for (x,y,w,h) in faces:
        face_img = img[y:y+h, x:x+w]
        face_imgs.append(face_img)
        # draw rectangle around face on img
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0, 255),4)

# plot image with face detected
plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)) 
plt.title("Detected Face")
plt.show()