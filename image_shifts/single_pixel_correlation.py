import cv2 as cv
import numpy as np
import os
import sys
import csv
from scipy.signal import correlate
from scipy.stats import pearsonr
import matplotlib.pyplot as plt


def calculate_correlation_for_wells(well, nbRows, nbCols, base_path, base_name, img1_suffix, img2_suffix, segmentation_base_path, segmentation_base_name, save_as_csv, background_threshold = 115):
    results = [['Well', 'Site_x', 'Site_y', 'Label', 'PearsonR']] # List containing well & site for each cell measured

    for j in range(nbCols):
        for i in range(nbRows):
            x = '_x%03d' %i
            y = '_y%03d' %j
            # 2 channels: each has a background threshold
            path_1 = os.path.join(base_path, base_name + well + y + x + img1_suffix)
            path_2 = os.path.join(base_path, base_name + well + y + x + img2_suffix)
            print(well + y + x)
            segmentation_path = os.path.join(segmentation_base_path, segmentation_base_name + well + '_x' + str(i) + 'y' + str(j) + '.png')
            curr_correlation = calculate_single_pixel_correlation_all_cells(path1 = path_1, path2 = path_2, segmentation_path = segmentation_path, background_threshold= background_threshold)
            curr_site_info = [[well, i, j]] * len(curr_correlation)
            list_results = [[a[0][0], a[0][1], a[0][2], a[1][0], a[1][1]] for a in zip(curr_site_info, curr_correlation)]
            results.extend(list_results)
    print(results)
    if save_as_csv:
        filename = 'SinglePixelCorrelation' + well + '.csv'
        with open(filename, 'wb') as f1:
            wr = csv.writer(f1)
            wr.writerows(results)


def calculate_single_pixel_correlation_all_cells(path1, path2, segmentation_path, background_threshold):
    correlations = []
    # Load images
    img1 = cv.imread(path1, -1).astype('int64')
    img2 = cv.imread(path2, -1).astype('int64')

    # Load segmentation
    segmentation = cv.imread(segmentation_path, -1)

    label_list = np.unique(segmentation)
    for label in label_list[1:]:
        curr_cell = segmentation == label

        # Mask with segmentation
        img1_masked = img1[curr_cell]
        img2_masked = img2[curr_cell]

        # Remove outliers (a few pixels may have very high values => remove those)
        outliers = np.zeros(img1_masked.shape)
        outliers[img1_masked > 60000] = 1
        outliers[img2_masked > 60000] = 1

        # Substract background
        img1_back_subs = img1_masked[~outliers.astype('bool')] - background_threshold
        img2_back_subs = img2_masked[~outliers.astype('bool')] - background_threshold

        # Correlate images
        # output = correlate(img1_back_subs, img2_back_subs, mode = 'valid')
        plt.plot(img1_back_subs, img2_back_subs, 'o' , markersize=1)
        plt.show()
        print(pearsonr(img1_back_subs, img2_back_subs)[0])
        correlations.append([label, pearsonr(img1_back_subs, img2_back_subs)[0]])

    return correlations


nbRows = 6
nbCols = 6
well_list = []
for row in ['B', 'C', 'D', 'E', 'F', 'G']:
    for col in range(2,12):
        well_name = row + '%02d' % col
        well_list.append(well_name)

input_ind = int(sys.argv[1])
# input_ind = 0
currWell = well_list[input_ind]

calculate_correlation_for_wells(well=currWell, nbRows=nbRows, nbCols=nbCols,
                base_path='/Users/Joel/shares/dataShareJoel/jluethi/20180322-ShrinkageTest2/20180324_ShrinkageTest2_IllumCorr_images/',
                base_name='20180324_ShrinkageTest2_p1_', img1_suffix='_z000_t000_0_A02_C02.png',
                img2_suffix='_z000_t000_1_A02_C02.png', segmentation_base_path = "/Users/Joel/shares/dataShareJoel/jluethi/20180322-ShrinkageTest2/Segmentations",
                segmentation_base_name = "20180324_ShrinkageTest2Segmentation_Cells_plate_p1_well_",
                save_as_csv=True, background_threshold = 115)
