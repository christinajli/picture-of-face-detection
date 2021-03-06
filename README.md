# Real face detection 

One of my pet peeve in movies and tv shows is characters hacking a facial regonition security with a picture. Breaking in billionaire's vault with just an ipad? Well, that's just lazy writing. Even without using 3d sensors, liveness detection algorithms developed by others such as [Prabhat Ale](https://github.com/prabhat-123/Face_Antispoofing_System) and [Adrian Rosebrock](https://www.pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/) can easily tell a real face from a picture of a face. 

Below are my two solutions to distinguishing between a real face and a picture of a face.

## Solution #1: planar transformation of pictures

Assume the given data consists of the same picture of a face in frontal view, either printed on a flat surface or presented on a screen, and the picture is shown in all three angles (left, center, and right). The angled images is certain to be some planar transformation of each other. Perspective transformation is used because it covers a wide range of transformation such as rotation, translation, and non-isotopic scaling. If there exist some valid transformation matrix that describes the transformation taken by the planar surfaces, then the system can conclude that the images are of a picture of a face, and by assumption, any data that is not pictures of a face, are real faces. 


## Solution #2: camera face detection

This programs opens the camera and attempts to match frontal and side profiles of face with the Haar Cascade algorithm in real time. If valid faces are found for all three sides, it determines the face is real and not a picture. This does not account for three separate picture of faces in all three angles (left, center, and right)


## Requirements
The program requires the following to run:
- Python v2.7 or above
- OpenCV
- NumPy
- Webcam


## Result for solution #1
A picture of a face is displayed on a tablet, and images are taken by facing the tablet to the center, right, and left of the camera. The faces are correctly identified by using Haar Cascade algorithm, and are enclosed in a blue rectangle.

<p float="left">
    <img src="https://github.com/christinajli/picture-of-face-detection/blob/master/readme-imgs/detect_face_data_center.png" width="250" height="250" />
    <img src="https://github.com/christinajli/picture-of-face-detection/blob/master/readme-imgs/detect_face_data_right.png" width="250" height="250" />
    <img src="https://github.com/christinajli/picture-of-face-detection/blob/master/readme-imgs/detect_face_data_left.png" width="250" height="250" />
</p>
Keypoints from the faces are detected by the SIFT Detector, and the computed descriptors are passed to a FLANN based matcher. The following images show that featurs are being matched up from two detected face images. 

<p float="left">
    <img src="https://github.com/christinajli/picture-of-face-detection/blob/master/readme-imgs/matching_center_right.png" width="250" height="250" />
    <img src="https://github.com/christinajli/picture-of-face-detection/blob/master/readme-imgs/matching_center_left.png" width="250" height="250" />
    <img src="https://github.com/christinajli/picture-of-face-detection/blob/master/readme-imgs/matching_right_left.png" width="250" height="250" />
</p>