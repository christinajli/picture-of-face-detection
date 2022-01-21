import cv2
import os
from matplotlib import pyplot as plt
import numpy as np

AVERGAE_ERROR_THRESHOLD = 100
LOWE_MATCHES_THRESHOLD = 20
RATIO_TEST_THRESHOLD = 0.8

# Detect face region
def get_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    frontal_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = frontal_face_cascade.detectMultiScale(gray, 1.1, 10)
    
    # if no frontal face detected, check left profile face
    if len(faces)==0: 
        profile_face_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
        faces = profile_face_cascade.detectMultiScale(gray, 1.1, 10)
    
    # check right profile face
    if len(faces)==0: 
        # haarcascade_profileface trained with left profile of face, need to flip the image to detect right side
        flipped = cv2.flip(gray, 1)
        profile_face_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
        faces = profile_face_cascade.detectMultiScale(flipped, 1.1, 10)

    # extract the area of the face only
    if len(faces)!=0: 
        for (x,y,w,h) in faces:
            face_img = img[y:y+h, x:x+w]
            # uncomment to show detected face 
            # cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),4)
    else:
        # if still no face detected, then return original image
        return img

    # uncomment to show detected face
    # plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)) 
    # plt.title("Detected Face")
    # plt.show()
    
    return face_img


# Match two faces
def matching(img_a, img_b):
    new_img_a = img_a.copy()
    new_img_b = img_b.copy()
    
    my_SIFT_instance = cv2.SIFT_create()
    kp_a, des_a = my_SIFT_instance.detectAndCompute(new_img_a, None)
    kp_b, des_b = my_SIFT_instance.detectAndCompute(new_img_b, None)
    
    flann = cv2.FlannBasedMatcher()
    matches = flann.knnMatch(des_a, des_b, k=2)
    
    filtered_matches=[]
    draw_matches = []
    for m, n in matches: 
        if m.distance < RATIO_TEST_THRESHOLD*n.distance:
            filtered_matches.append(m)
            draw_matches.append([m])
    
    # uncomment to see key points matching result
    # new_img_a = cv2.drawKeypoints(new_img_a, kp_a,new_img_a)
    # new_img_b = cv2.drawKeypoints(new_img_b, kp_b,new_img_b)
    
    # matches_img = cv2.drawMatchesKnn(new_img_a,kp_a,new_img_b,kp_b,draw_matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # plt.imshow(matches_img, cmap = 'gray') 
    # plt.title("Face Result")
    # plt.show()

    return kp_a, des_a, kp_b, des_b, filtered_matches


# Detect if face region undergo transformation
def check_transformation(img_a, img_b):
    reference_img = cv2.cvtColor(img_a,cv2.COLOR_BGR2GRAY)
    test_img = cv2.cvtColor(img_b,cv2.COLOR_BGR2GRAY)
    
    kp_ref, des_ref, kp_rot, des_rot, lowe_matches = matching(reference_img, test_img)
    
    # if not enough matches are found, no need to find homography matrix, return large value
    if (len(lowe_matches) < LOWE_MATCHES_THRESHOLD):
        return 10000
    
    ref_pts = np.float32(np.array([kp_ref[m.queryIdx].pt for m in lowe_matches]).reshape(-1,1,2))
    img_pts = np.float32(np.array([kp_rot[m.trainIdx].pt for m in lowe_matches]).reshape(-1,1,2))
    homography_matrix, _ = cv2.findHomography(ref_pts,img_pts,cv2.RANSAC)
    
    error_distance = 0
    for i in range(len(ref_pts[0])):
        # Take points of reference image and reproject them using the computed homography matrix
        a_point = (ref_pts[0][i][0], ref_pts[0][i][1], 1)
        computed_point = np.matmul(homography_matrix, a_point)

        # Calculate the euclidean distance between the reprojected points and the real points in the image
        error_distance += np.sqrt(np.square(computed_point[0]-img_pts[0][0][0]) + np.square(computed_point[1]-img_pts[0][0][1]) + np.square(computed_point[2]-1))

    error_distance = error_distance/len(ref_pts[0])
    
    # uncomment to see error distance
    # print("error distance", error_distance)

    return error_distance


# Evaluation 
def get_result(res1,res2,res3):
    average_error = (res1 + res2 + res3)/3

    # uncomment to see average error for three comparisons
    # print ('avg error', average_error)
    
    # check threshold for average error distance
    if (average_error < AVERGAE_ERROR_THRESHOLD):
        print("The face is a picture")
    else:
        print("The face is real")