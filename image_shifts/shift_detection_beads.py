# Copyright (C) 2018 Joel Luethi, University of Zurich
# Script to detect the shift between channels using multifluorescent beads
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pickle
import os

def find_beads_centers(image_path, kernelsize, threshold):

    # detect the center of the spot and return a list of its coordinates
    bead_centers = []
    img = cv.imread(image_path, -1)
    img_blurred = cv.GaussianBlur(img,(5,5),0)
    threshholded_img = np.array(img_blurred >= threshold, dtype=np.uint8)

    # Remove small spots by morphological opening
    kernel = np.ones((kernelsize,kernelsize),np.uint8)
    img_big_spots = cv.morphologyEx(threshholded_img, cv.MORPH_OPEN, kernel)
    # Find all objects and their center
    a, contours,hierarchy = cv.findContours(img_big_spots, 1, 2)
    for spot in contours:
        M = cv.moments(spot)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        bead_centers.append((cy, cx))
        # All values are in the y, x format, as the img ndarray uses the y information first
    return bead_centers

def match_bead_centers(image_dims, distance_threshold, path1, path2, threshold1, threshold2):
    # Match bead centers, find all minimal distance matches
    # If two bead centers are more than the distance_threshold away from each other in manhattan distance,
    # they are not considered to be the same bead
    # Returns a list of bead positions in img1 & the x & y shifts in image 2 (so that img2 needs to be shifted by the amount specified to get the desired result
    bead_centers_1 = find_beads_centers(path1, kernelsize=5, threshold=threshold1)
    bead_centers_2 = find_beads_centers(path2, kernelsize=5, threshold=threshold2)

    # shifts contain the position in img1 and the x,y shift to img 1: [(xpos, ypos),(xshift, yshift)]
    shifts = []

    # List all potential matches. The list contains the location of center1, the location of center2 and the distance between them
    distance_to_1 = []
    for center1 in bead_centers_1:
        curr_distances = []
        for center2 in bead_centers_2:
            # If center1 & center2 are less than distance_threshold appart: Add them as a potential match. Use manhattan distance
            dist = abs(center1[0] - center2[0]) + abs(center1[1] - center2[1])
            if dist < distance_threshold:
                curr_distances.append((center1, center2,dist))

        distance_to_1.append(curr_distances)

    # Prune list of matches to just 1 per bead: If it's a simple case (1-to-1 matches), just keep it. Otherwise, optimize
    # Check length of sublists
    nb_of_neighbors = []
    for element in distance_to_1:
        nb_of_neighbors.append(len(element))

    # If there are no beads in this site, return an empty list
    if not nb_of_neighbors:
        print('No beads in this site')
        return shifts

    # If the match is ambiguous, remove the bead from consideration
    if max(nb_of_neighbors) > 1:
        for j in range(len(distance_to_1)-1, -1, -1):
            # Go through the list in reverse, check for each element whether it has more than one potential match. Remove those
            if len(distance_to_1[j]) > 1:
                print('Removing a bead with multiple potential matches in channel 2')
                del distance_to_1[j]

    # If there is no match for a bead in img1, remove that bead from consideration
    if min(nb_of_neighbors) == 0:
        for j in range(len(distance_to_1)-1, -1, -1):
            # Go through the list in reverse, check for each element whether it's an empty list. If so, remove it.
            if not distance_to_1[j]:
                print('Removing a bead without matches in channel 2')
                del distance_to_1[j]

    for bead in distance_to_1:
        corr_center1 = bead[0][0]
        corr_center2 = bead[0][1]
        curr_xshift = corr_center1[1] - corr_center2[1]
        curr_yshift = corr_center1[0] - corr_center2[0]
        shifts.append([corr_center1, (curr_xshift, curr_yshift)])

    return (shifts)


def calculate_bead_shifts_multiple_sites(nbSites, base_path, base_name, img1_suffix, img2_suffix, dist_threshold = 30, image_dimensions = (2160,2560), save_as_pickle = False, threshold_1 = 140, threshold_2 = 140):
    # Use this list initialization to make each list an independent object (otherwise they all contain all of the shift information)
    x_shift_list = [[[] for j in range(image_dimensions[1])] for i in range(image_dimensions[0])]
    y_shift_list = [[[] for j in range(image_dimensions[1])] for i in range(image_dimensions[0])]

    shifts = []

    for i in range(1, nbSites + 1):
        site = '%03d' %i
        print('Site ' + str(i))
        # 2 channels: each has a background threshold and
        path_green = os.path.join(base_path, base_name + site + img1_suffix)
        path_red = os.path.join(base_path, base_name + site + img2_suffix)

        shifts += match_bead_centers(image_dimensions, distance_threshold= dist_threshold, path1 = path_red, path2 = path_green, threshold1 = threshold_1, threshold2 = threshold_2)

    if save_as_pickle:
        # To avoid rerunning the actual calculations to many times, pickle the to shift lists => easy access for later
        with open('all_shifts_60x_blue_red_corrected_preAlignment.pkl', 'wb') as f1:
            pickle.dump(shifts, f1)

    return (shifts)


image_dimensions = (2160, 2560)
dist_threshold = 20
nbSites = 63


# all_shifts = calculate_bead_shifts_multiple_sites(nbSites = nbSites, dist_threshold = dist_threshold, base_path='/Users/Joel/shares/dataShareJoel/jluethi/20180312_BeadsShift_60x_PostCVAlignment/images/',
#                                      base_name= 'AssayPlate_Greiner_655896_F04_T0001F', img1_suffix= 'L01A01Z01C02.tif', img2_suffix='L01A02Z01C01.tif', save_as_pickle = True)
all_shifts = calculate_bead_shifts_multiple_sites(nbSites = nbSites, dist_threshold = dist_threshold, base_path='/Users/Joel/shares/dataShareJoel/jluethi/20180219-FixationTest/Cycle10_images/',
                                     base_name= 'AssayPlate_Greiner_655896_F04_T0001F', img1_suffix= 'L01A01Z01C01.tif', img2_suffix='L01A02Z01C03.tif', save_as_pickle = False, threshold_1 = 135, threshold_2 = 140)

# Read in the pickle lists
# with open('all_shifts_60x_CV7K_Camera_Aligned.pkl', 'rb') as f1:
#     all_shifts = pickle.load(f1)

print('Total number of beads:', str(len(all_shifts)))

# Create an image of the pixel shifts
x_shift = np.zeros(image_dimensions)
y_shift = np.zeros(image_dimensions)
nb_beads = np.zeros(image_dimensions)

# Reverse sliding window: For every sample, check which area should be affected
window_size = 200
for shift in all_shifts:
    # print(shift)
    # Define the are to be affected in the image
    ymin = max(shift[0][0] - window_size, 0)
    xmax = abs(max(shift[0][1] - window_size, 0) - image_dimensions[1])
    ymax = min(shift[0][0] + window_size, image_dimensions[0])
    xmin = abs(min(shift[0][1] + window_size, image_dimensions[1]) - image_dimensions[1])

    y_shift[ymin:ymax, xmin:xmax] += shift[1][0]
    x_shift[ymin:ymax, xmin:xmax] += shift[1][1]
    nb_beads[ymin:ymax, xmin:xmax] += 1

y_shift_corrected = y_shift
y_shift_corrected[nb_beads != 0] = y_shift[nb_beads != 0] / nb_beads[nb_beads != 0]
x_shift_corrected = x_shift
x_shift_corrected[nb_beads != 0] = x_shift[nb_beads != 0] / nb_beads[nb_beads != 0]

plt.imshow(y_shift_corrected, cmap="hot")
plt.colorbar()
plt.show()
plt.imshow(x_shift_corrected, cmap="hot")
plt.colorbar()
plt.show()
np.save('x_shift_corrected_20180302_60x_corrected.npy', x_shift_corrected)
np.save('y_shift_corrected_20180302_60x_corrected.npy', y_shift_corrected)













