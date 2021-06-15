import cv2
from cv2 import imshow
import argparse

#from google.colab.patches import cv2_imshow
#img = cv2.imread('brain-scan-ADHD.jpeg')
#img.shape
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True, help='path to img')
args = vars(ap.parse_args())
imgpath = args["image"]
img = cv2.imread(imgpath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2_imshow(gray)
ksize = [-1, 3]
gx = cv2.Sobel(gray,ddepth = cv2.CV_32F, dx=1, dy=0, ksize= ksize[0])
gy = cv2.Sobel(gray,ddepth = cv2.CV_32F, dx=0, dy=1, ksize= ksize[0])
gx = cv2.convertScaleAbs(gx)
gy = cv2.convertScaleAbs(gy)
gx3 = cv2.Sobel(gray,ddepth = cv2.CV_32F, dx=1, dy=0, ksize= ksize[1])
gy3 = cv2.Sobel(gray,ddepth = cv2.CV_32F, dx=0, dy=1, ksize= ksize[1])
gx3 = cv2.convertScaleAbs(gx3)
gy3 = cv2.convertScaleAbs(gy3)
#Sobel-> linear-> ksize = -1
# Scharr -> ksize->3i
combine = cv2.addWeighted(gx, 0.5, gy, 0.5, 0)
combine3 = cv2.addWeighted(gx3, 0.5, gy3, 0.5, 0)
import numpy as np
magnitude = np.sqrt((gx**2) + (gy**2))
import matplotlib.pyplot as plt
(fig, axs) = plt.subplots(nrows=1, ncols=3, figsize=(8,4))
axs[0].imshow(gray, cmap='gray')
mag = magnitude.astype(int)
orientation = np.arctan2(gx,gy) * (180/ np.pi) % 180
axs[1].imshow(mag, cmap='jet')
ornt = orientation.astype(int)
axs[2].imshow(ornt, cmap='jet')
plt.tight_layout()
plt.show()
