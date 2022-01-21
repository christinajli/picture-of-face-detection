import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
from helper import get_face, check_transformation, get_result

# read in images and get face from images
face_img1 = get_face(cv2.imread("data/data_center.jpg"))
face_img2 = get_face(cv2.imread("data/data_right.jpg"))
face_img3 = get_face(cv2.imread("data/data_left.jpg"))

# check transformation between two sets of faces
result1 = check_transformation(face_img1, face_img2)
result2 = check_transformation(face_img1, face_img3)
result3 = check_transformation(face_img2, face_img3)

# evaluate matrix error
get_result(result1, result2, result3)
