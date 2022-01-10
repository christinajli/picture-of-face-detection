import cv2
import numpy as np
import glob
import os

# delete previously saved images
fileList = glob.glob('camera_*.jpeg')
for file in fileList:
    try:
        os.remove(file)
        print("removed " + file)
    except:
        print("Error while deleting file : ", file)

cam = cv2.VideoCapture(0)
window_name = "Capture sample data"
cv2.namedWindow(window_name)

img_counter = 0
is_flipped = False

# variables to display text
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0, 0, 255)
thickness = 2
instructions = "Press Esc to leave. "

# detect front/center of face
frontal_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# detect profile of face
profile_face_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

while img_counter < 3:
    ret, frame = cam.read()
    if not ret:
        print("Failed to open camera")
        break

    # flip camera to mirror, can be a bit slow
    # frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if img_counter == 0:
        text = instructions + "Look directly at the camera and press the Space-bar"
        img_name = "camera_center.jpeg"
        # set minNeighbor to high to avoid false positives since by assumption, only one face per image
        faces = frontal_face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)

    if img_counter == 1:
        text = instructions + "Look to the left and press the Space-bar"
        img_name = "camera_right.jpeg"
        # haarcascade_profileface trained with left profile of face, need to flip the image to detect right side
        flipped = cv2.flip(gray, 1)
        faces = profile_face_cascade.detectMultiScale(flipped, scaleFactor=1.2, minNeighbors=10)
        is_flipped = True

    if img_counter == 2:
        is_flipped = False
        text = instructions + "Look to the right and press the Space-bar"
        img_name = "camera_left.jpeg"
        faces = profile_face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)

    # get boundary of the text
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    # get coords based on boundary 
    textX = (frame.shape[1] - textsize[0]) // 2
    textY = (frame.shape[0] - textsize[1])
    coords = (textX, textY)

    frame = cv2.putText(frame, text, coords, font, fontScale, color, thickness, cv2.LINE_AA, False)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        if is_flipped: 
            cv2.rectangle(frame, (frame.shape[1]-x-w, y), (frame.shape[1]-x, y+h), (0, 0, 255), 2)
            face_img = frame[y:y+h, frame.shape[1]-x-w:frame.shape[1]-x]
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            face_img = frame[y:y+h, x:x+w]

    cv2.imshow(window_name, frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # Esc key
        print("Closing window...")
        break
    elif k%256 == 32:
        # Space-bar
        # only take picture when face is in frame
        if (len(faces)!= 0) and (face_img.any()):
            cv2.imwrite(img_name, face_img)
            print("{} image saved!".format(img_name))
            img_counter += 1
            faces = None
            face_img = None

cam.release()
cv2.destroyWindow(window_name)

if os.path.isfile("camera_left.jpeg") and os.path.isfile("camera_center.jpeg") and os.path.isfile("camera_right.jpeg"):
    print("The face is real")
else:
    print("Not enough data provided or the face is a picture")