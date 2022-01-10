# Copyright (C) 2018 Joel Luethi, University of Zurich
# Script to correct an image for the detected shifts (based on beads)
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pickle
import os
from scipy.ndimage.filters import gaussian_filter

x_shift = np.load('x_shift_corrected_20180219_Beads_mirrored.npy')
y_shift = np.load('y_shift_corrected_20180219_Beads_mirrored.npy')

upscale_factor = 5
image_dimensions = (2160, 2560)
upscaled_dimensions = (10800, 12800)
# upscaled_dimensions = (21600, 25600)

# Smooth the shift img (try smoothing after resizing)
# x_shift_smoothed = gaussian_filter(input= x_shift, sigma = 5) * upscale_factor
# y_shift_smoothed = gaussian_filter(input= y_shift, sigma = 5) * upscale_factor
# plt.imshow(x_shift_smoothed, cmap="hot")
# plt.colorbar()
# plt.show()

upscaled_x_shift = cv.resize(x_shift, None, fx = upscale_factor, fy = upscale_factor)
# Smooth the shift img (try smoothing after resizing)
x_shift_smoothed = gaussian_filter(input= upscaled_x_shift, sigma = 5) * upscale_factor
upscaled_x_shift_rounded = np.rint(x_shift_smoothed).astype(int)


upscaled_y_shift = cv.resize(y_shift, None, fx = upscale_factor, fy = upscale_factor)
# Smooth the shift img (try smoothing after resizing)
y_shift_smoothed = gaussian_filter(input= upscaled_y_shift, sigma = 5) * upscale_factor
upscaled_y_shift_rounded = np.rint(y_shift_smoothed).astype(int)

img = cv.imread('/Users/Joel/shares/dataShareJoel/jluethi/20180219-FixationTest/ElutionRestain_images/AssayPlate_Greiner_655896_F04_T0001F063L01A03Z01C02.tif', -1)
upscaled_img = cv.resize(img, None, fx = upscale_factor, fy = upscale_factor)
upscaled_target = np.zeros(upscaled_dimensions)

for y in range(upscaled_dimensions[0]):
    for x in range(upscaled_dimensions[1]):
        new_y = y + upscaled_y_shift_rounded[y][x]
        new_x = x + upscaled_x_shift_rounded[y][x]
        if new_x < upscaled_dimensions[1] and new_x >= 0 and new_y < upscaled_dimensions[0] and new_y >= 0:
            upscaled_target[y][x] = upscaled_img[new_y][new_x]

downscaled_img = cv.resize(upscaled_target, None, fx = 1./upscale_factor, fy = 1./upscale_factor)
cv.imwrite('test_shift_corrected_F063_C02.png', downscaled_img.astype(np.uint16))





