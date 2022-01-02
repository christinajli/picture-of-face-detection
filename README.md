# Picture of Face Detection

The goal of the project is to differentiate between a set of images with a real face and a set of images with a picture of a face. Given three angled images of a face, in frontal, left, and right profiles, the program returns the probability of the given data being either real or a picture. This outcome is then compared with the existing liveness detection algorithms developed by others such as [Prabhat Ale](https://github.com/prabhat-123/Face_Antispoofing_System) and [Adrian Rosebrock](https://www.pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/). 

## Requirements
The program requires the following to run:
- Python v2.7 or above
- OpenCV
- NumPy
- Webcam

## Algorithm Overview

Assume the given data is the same picture of a face, either printed on a flat surface or presented on a screen, and the picture is shown in all three angles (left, center, and right). The angled images is certain to be some planar transformation of each other. Perspective transformation is used because it covers a wide range of transformation such as rotation, translation, and non-isotopic scaling. If there exist some valid transformation matrix that describes the transformation taken by the planar surfaces, then the system can conclude that the images are of a picture of a face, and by assumption, any data set that are not pictures of a face, are real faces. 

## To-Do

- [ ] 'x' button not close window popup with MacOS
- [x] right profile face rectangle need to be flipped because the image was flipped to detect the face
- [x] last face identified was saved when attempting to take image not in frame
- [x] capture_testing_data does not allow user take angled 2d picture of a face because the haarcascade_profileface.xml cannot detect profile of face to continue