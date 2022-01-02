# Picture of Face Detection

The goal of the project is to differentiate between a set of images with a real face and a set of images with a picture of a face. The program returns the probability of the given data being either real or a picture. This outcome is then compared with the existing liveness detection algorithms developed by others such as [Prabhat Ale](https://github.com/prabhat-123/Face_Antispoofing_System) and [Adrian Rosebrock](https://www.pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/). 

## Feature Requirements
- [x] open camera to take 3 images (left, center, and right) for testing
- [ ] read in images
- [ ] output face detected as real or picture with probability

## Algorithm Overview

If the given data is a picture of a face, either printed or presented on a screen, the face is on a flat surface in all three angles (left, center, and right). The angled images is certain to be some planar transformation of each other. Perspective transformation is used because it covers a wide range of transformation such as rotation, translation, and non-isotopic scaling. If there exist some valid transformation matrix that describes the transformation taken by the planar surfaces, then the system can conclude that the images are of a picture of a face, and by assumption, any data set that are not pictures of a face, are real faces. 

## Sample Data Usage

The GUI will open up the camera and take three images, users would need to follow the prompt to show left, center, and right side of face. The images are saved in the folder '/sample'. The program can also run on pre-existing images given three images named 'left.jpg', 'center.jpg', and 'right.jpg' in the '/testing_data' folder. 

Assuming there is only one face per image. 

## To-Do

- 'x' button on camera window popup might not close window with MacOS
- right profile face rectangle need to be flipped because the image was flipped to detect the face
- last face identified was saved when attempting to take image not in frame
- capture_testing_data does not allow user take angled 2d picture of a face because the haarcascade_profileface.xml cannot detect profile of face to continue