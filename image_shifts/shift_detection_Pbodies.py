# Copyright (C) 2018 Joel Luethi, University of Zurich
# Script to detect the shift between channels using multifluorescent beads
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pickle
import os
import csv
import sys
import math

def find_beads_centers(image_path, kernelsize, threshold):

    # detect the center of the spot and return a list of its coordinates
    bead_centers = []
    img = cv.imread(image_path, -1)
    img_blurred = cv.GaussianBlur(img,(3,3),0)
    threshholded_img = np.array(img_blurred >= threshold, dtype=np.uint8)

    # Remove small spots by morphological opening
    kernel = np.ones((kernelsize,kernelsize),np.uint8)
    img_big_spots = cv.morphologyEx(threshholded_img, cv.MORPH_OPEN, kernel)

    # Shot segmentation result
    # plt.imshow(img_big_spots)
    # plt.show()

    # Find all objects and their center
    a, contours,hierarchy = cv.findContours(img_big_spots, 1, 2)
    for spot in contours:
        M = cv.moments(spot)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        bead_centers.append((cy, cx, cv.contourArea(spot)))
        # All values are in the y, x format, as the img ndarray uses the y information first
    return bead_centers

def match_bead_centers(well, x, y, distance_threshold, path1, path2, threshold1, threshold2):
    # Match bead centers, find all minimal distance matches
    # If two bead centers are more than the distance_threshold away from each other in manhattan distance,
    # they are not considered to be the same bead
    # Returns a list of bead positions in img1 & the x & y shifts in image 2 (so that img2 needs to be shifted by the amount specified to get the desired result
    bead_centers_1 = find_beads_centers(path1, kernelsize=3, threshold=threshold1)
    bead_centers_2 = find_beads_centers(path2, kernelsize=3, threshold=threshold2)

    # shifts contain the position in img1 and the x,y shift to img 1: [(xpos, ypos),(xshift, yshift)]
    shifts = []
    # List all potential matches. The list contains the location of center1, the location of center2 and the distance between them
    distance_to_1 = []
    for center1 in bead_centers_1:
        curr_distances = []
        for center2 in bead_centers_2:
            # If center1 & center2 are less than distance_threshold apart: Add them as a potential match. Use manhattan distance
            dist = abs(center1[0] - center2[0]) + abs(center1[1] - center2[1])
            if dist < distance_threshold:
                curr_distances.append((center1, center2,dist))

        distance_to_1.append(curr_distances)

    # Prune list of matches to just 1 per bead: If it's a simple case (1-to-1 matches), just keep it. Otherwise, optimize
    # Check length of sublists
    nb_of_neighbors = []
    for element in distance_to_1:
        nb_of_neighbors.append(len(element))

    # print('A total of %d P bodies in this site' %len(distance_to_1))
    nb_objects = len(distance_to_1)

    # If there are no beads in this site, return an empty list
    if not nb_of_neighbors:
        print('No beads in this site')
        return shifts

    # If the match is ambiguous, remove the bead from consideration
    ambiguous_match_counter = 0
    if max(nb_of_neighbors) > 1:
        for j in range(len(distance_to_1)-1, -1, -1):
            # Go through the list in reverse, check for each element whether it has more than one potential match. Remove those
            if len(distance_to_1[j]) > 1:
                ambiguous_match_counter += 1
                del distance_to_1[j]
        # print('Removing %d P body with ambiguous matches in channel 2' % ambiguous_match_counter)

    # If there is no match for a bead in img1, remove that bead from consideration
    no_match_counter = 0
    if min(nb_of_neighbors) == 0:
        for j in range(len(distance_to_1)-1, -1, -1):
            # Go through the list in reverse, check for each element whether it's an empty list. If so, remove it.
            if not distance_to_1[j]:
                no_match_counter += 1
                del distance_to_1[j]
        # print('Removing %d P body without matches in channel 2' %no_match_counter)

    for bead in distance_to_1:
        corr_center1 = bead[0][0]
        corr_center2 = bead[0][1]
        curr_xshift = corr_center1[1] - corr_center2[1]
        curr_yshift = corr_center1[0] - corr_center2[0]
        euclidian_shift = math.sqrt(curr_xshift**2 + curr_yshift**2)
        shifts.append([well, x, y, corr_center1[0], corr_center1[1],corr_center1[2], corr_center2[2], euclidian_shift])

    return (shifts, nb_objects, ambiguous_match_counter, no_match_counter)

def calculate_bead_shifts_per_well(well, nbRows, nbCols, base_path, base_name, img1_suffix, img2_suffix, threshold_1, threshold_2, dist_threshold = 30, save_as_csv = False):
    shifts = [['Well', 'Site_x', 'Site_y', 'y_cor', 'x_cor', 'Area_1', 'Area_2', 'Shift']]
    nb_objects = 0
    ambiguous_match_counter = 0
    no_match_counter = 0

    for i in range(nbRows):
        for j in range(nbCols):
            x = '_x%03d' %i
            y = '_y%03d' %j
            # 2 channels: each has a background threshold
            path_1 = os.path.join(base_path, base_name + well + y + x + img1_suffix)
            path_2 = os.path.join(base_path, base_name + well + y + x + img2_suffix)
            print(well + y + x)
            site_results = match_bead_centers(well, i, j, distance_threshold= dist_threshold, path1 = path_1, path2 = path_2, threshold1 = threshold_1, threshold2 = threshold_2)
            if len(site_results) > 1:
                shifts += site_results[0]
                nb_objects += site_results[1]
                ambiguous_match_counter += site_results[2]
                no_match_counter += site_results[3]

    print('A total of %d P bodies in well ' % nb_objects)
    print('Removing %d P bodies with ambiguous matches in channel 2' % ambiguous_match_counter)
    print('Removing %d P body without matches in channel 2' % no_match_counter)

    if save_as_csv:
        filename = 'Pbodies_shift_' + well + '.csv'
        with open(filename, 'wb') as f1:
            wr = csv.writer(f1)
            wr.writerows(shifts)

    return (shifts)


# path_1 = '/Users/Joel/shares/dataShareJoel/jluethi/20180322-ShrinkageTest2/20180324_ShrinkageTest2_IllumCorr_images/20180324_ShrinkageTest2_p1_B02_y000_x000_z000_t000_0_A02_C02.png'
# path_2 = '/Users/Joel/shares/dataShareJoel/jluethi/20180322-ShrinkageTest2/20180324_ShrinkageTest2_IllumCorr_images/20180324_ShrinkageTest2_p1_B02_y000_x000_z000_t000_1_A02_C02.png'
# all_shifts = match_bead_centers(distance_threshold= 15, path1 = path_1, path2 = path_2, threshold1 = 600, threshold2 = 600)

dist_threshold = 15
nbRows = 6
nbCols = 6
well_list = []
for row in ['B', 'C', 'D', 'E', 'F', 'G']:
    for col in range(2,12):
        well_name = row + '%02d' % col
        well_list.append(well_name)


# Input goes from 1 to 60 here
#input_ind = int(sys.argv[1])
input_ind = 6
currWell = well_list[input_ind]

all_shifts = calculate_bead_shifts_per_well(well = currWell, nbRows = nbRows, nbCols = nbCols, dist_threshold = dist_threshold, base_path='/Users/Joel/shares/dataShareJoel/jluethi/20180322-ShrinkageTest2/20180324_ShrinkageTest2_IllumCorr_images/',
                                     base_name= '20180324_ShrinkageTest2_p1_', img1_suffix= '_z000_t000_0_A02_C02.png', img2_suffix='_z000_t000_1_A02_C02.png', save_as_csv = True, threshold_1 = 500, threshold_2 = 500)





# Read in the pickle lists
# with open('all_shifts_60x_CV7K_Camera_Aligned.pkl', 'rb') as f1:
#     all_shifts = pickle.load(f1)

# print('Total number of beads:', str(len(all_shifts)))
#
# # Create an image of the pixel shifts
# x_shift = np.zeros(image_dimensions)
# y_shift = np.zeros(image_dimensions)
# nb_beads = np.zeros(image_dimensions)
#
# # Reverse sliding window: For every sample, check which area should be affected
# window_size = 200
# for shift in all_shifts:
#     # print(shift)
#     # Define the are to be affected in the image
#     ymin = max(shift[0][0] - window_size, 0)
#     xmax = abs(max(shift[0][1] - window_size, 0) - image_dimensions[1])
#     ymax = min(shift[0][0] + window_size, image_dimensions[0])
#     xmin = abs(min(shift[0][1] + window_size, image_dimensions[1]) - image_dimensions[1])
#
#     y_shift[ymin:ymax, xmin:xmax] += shift[1][0]
#     x_shift[ymin:ymax, xmin:xmax] += shift[1][1]
#     nb_beads[ymin:ymax, xmin:xmax] += 1
#
# y_shift_corrected = y_shift
# y_shift_corrected[nb_beads != 0] = y_shift[nb_beads != 0] / nb_beads[nb_beads != 0]
# x_shift_corrected = x_shift
# x_shift_corrected[nb_beads != 0] = x_shift[nb_beads != 0] / nb_beads[nb_beads != 0]
#
# plt.imshow(y_shift_corrected, cmap="hot")
# plt.colorbar()
# plt.show()
# plt.imshow(x_shift_corrected, cmap="hot")
# plt.colorbar()
# plt.show()
# np.save('x_shift_corrected_20180302_60x_corrected.npy', x_shift_corrected)
# np.save('y_shift_corrected_20180302_60x_corrected.npy', y_shift_corrected)













