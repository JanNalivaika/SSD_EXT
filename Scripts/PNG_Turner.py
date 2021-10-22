import numpy as np
import cv2
import os


def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

path = "../Output/HD_pictures/HD_left_rotation_0.png"
image = cv2.imread(path)


output_path = r'../Output/TurnedPNG'
if not os.path.exists(output_path):
  os.makedirs(output_path)


for angle in range(91):
  test = rotate_image(image, angle)
  cv2.imwrite("../Output/TurnedPNG/" + str(angle) + ".png", test)
