import cv2
import numpy as np
img = cv2.imread('/home/ros/image.jpg')
imgB = np.add(img,50)
cv2.imwrite('imb.jpg',imgB)
