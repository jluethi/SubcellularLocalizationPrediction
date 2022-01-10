import cv2 as cv
import numpy as np
import os
import sys
import csv
from scipy.stats import pearsonr
import pandas as pd
# import matplotlib.pyplot as plt


def calculate_correlation_for_wells(well, base_path, base_name, img1_suffix, img2_suffix, segmentation_base_path, segmentation_base_name, save_as_csv, metadata_filename, background_threshold = 115):
    results = [['Well', 'Site_x', 'Site_y', 'Label', 'PearsonR']] # List containing well & site for each cell measured
    metadata = load_tm_metadata(metadata_filename)
    cells_in_well = metadata[metadata.well_name == well]
    x_pos_list = cells_in_well.well_pos_x.unique()

    # Loop through all the x positions
    for x_pos in x_pos_list:
        cells_at_xpos = cells_in_well[cells_in_well.well_pos_x == x_pos]
        y_pos_list = cells_at_xpos.well_pos_y.unique()

        # Loop through all the y positions
        for y_pos in y_pos_list:
            site_of_interest = cells_at_xpos[cells_at_xpos.well_pos_y == y_pos]
            label_list = site_of_interest.label.unique()
            x = '_x%03d' % x_pos
            y = '_y%03d' % y_pos
            # 2 channels: each has a background threshold
            path_1 = os.path.join(base_path, base_name + well + y + x + img1_suffix)
            path_2 = os.path.join(base_path, base_name + well + y + x + img2_suffix)
            print(well + y + x)
            segmentation_path = os.path.join(segmentation_base_path, segmentation_base_name + well + '_x' + str(x_pos) + 'y' + str(y_pos) + '.png')
            curr_correlation = calculate_single_pixel_correlation_all_cells(path1 = path_1, path2 = path_2,
                                                                            segmentation_path = segmentation_path,
                                                                            background_threshold= background_threshold,
                                                                            label_list = label_list)
            curr_site_info = [[well, x_pos, y_pos]] * len(curr_correlation)
            list_results = [[a[0][0], a[0][1], a[0][2], a[1][0], a[1][1]] for a in zip(curr_site_info, curr_correlation)]
            results.extend(list_results)
    print(results)
    if save_as_csv:
        filename = 'SinglePixelCorrelation_' + img1_suffix[11:-4] + '_' + img2_suffix[11:-4] + '.csv'
        if os.path.isfile(filename):
            with open(filename, 'ab') as f1:
                wr = csv.writer(f1)
                wr.writerows(results)
        else:
            with open(filename, 'wb') as f1:
                wr = csv.writer(f1)
                wr.writerows(results)


def calculate_single_pixel_correlation_all_cells(path1, path2, segmentation_path, background_threshold, label_list):
    correlations = []
    # Load images
    img1 = cv.imread(path1, -1).astype('int64')
    img2 = cv.imread(path2, -1).astype('int64')

    # Load segmentation
    segmentation = cv.imread(segmentation_path, -1)

    for label in label_list:
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

        # Set negative values to 0
        img1_back_subs[img1_back_subs < 0] = 0
        img2_back_subs[img2_back_subs < 0] = 0

        # Correlate images
        # output = correlate(img1_back_subs, img2_back_subs, mode = 'valid')
        # plt.plot(img1_back_subs, img2_back_subs, 'o' , markersize=1)
        # plt.show()
        # print(pearsonr(img1_back_subs, img2_back_subs)[0])
        correlations.append([label, pearsonr(img1_back_subs, img2_back_subs)[0]])

    return correlations

def load_tm_metadata(metadata_filepath):
    metadata = pd.read_csv(metadata_filepath, header=0)
    total_cells = len(metadata)
    # Delete cells that are classified as 1 by any of the classifiers and remove the classifiers from the data frame
    metadata = metadata[(metadata.is_border == 0) & (metadata.DAPI_Debris == 0) &
                        (metadata.Mitotic == 0) & (metadata.Multinuclei == 0)]

    print "Discarding " + str(total_cells - len(metadata)) + ' of ' + str(total_cells) + ' cells, because of classifiers'

    del metadata['is_border']
    del metadata['DAPI_Debris']
    del metadata['Mitotic']
    del metadata['Multinuclei']
    return metadata

# List of pairs of img1_suffix & img2_suffix to be compared
staining_combination = [['_z000_t000_2_Calreticulin.png', '_z000_t000_8_Caveolin.png'],
                        ['_z000_t000_2_Calreticulin.png', '_z000_t000_10_Pericentrin.png'],
                        ['_z000_t000_8_Caveolin.png', '_z000_t000_10_Pericentrin.png'],
                        ['_z000_t000_n2_EEA1.png', '_z000_t000_8_Pol2.png'],
                        ['_z000_t000_n2_EEA1.png', '_z000_t000_10_Paxillin.png'],
                        ['_z000_t000_8_Pol2.png', '_z000_t000_10_Paxillin.png'],
                        ['_z000_t000_3_APPL.png', '_z000_t000_5_pS6.png'],
                        ['_z000_t000_3_APPL.png', '_z000_t000_7_Actin.png'],
                        ['_z000_t000_3_APPL.png', '_z000_t000_11_Sara.png'],
                        ['_z000_t000_3_APPL.png', '_z000_t000_13_DDX6.png'],
                        ['_z000_t000_5_pS6.png', '_z000_t000_7_Actin.png'],
                        ['_z000_t000_5_pS6.png', '_z000_t000_11_Sara.png'],
                        ['_z000_t000_5_pS6.png', '_z000_t000_13_DDX6.png'],
                        ['_z000_t000_7_Actin.png', '_z000_t000_11_Sara.png'],
                        ['_z000_t000_7_Actin.png', '_z000_t000_13_DDX6.png'],
                        ['_z000_t000_11_Sara.png', '_z000_t000_13_DDX6.png'],
                        ['_z000_t000_3_GM130.png', '_z000_t000_5_Yap.png'],
                        ['_z000_t000_3_GM130.png', '_z000_t000_11_EEA1.png'],
                        ['_z000_t000_3_GM130.png', '_z000_t000_13_DCP1a.png'],
                        ['_z000_t000_5_Yap.png', '_z000_t000_11_EEA1.png'],
                        ['_z000_t000_5_Yap.png', '_z000_t000_13_DCP1a.png'],
                        ['_z000_t000_11_EEA1.png', '_z000_t000_13_DCP1a.png'],
                        ['_z000_t000_2_Calreticulin.png', '_z000_t000_n2_EEA1.png'],
                        ['_z000_t000_2_Calreticulin.png', '_z000_t000_3_APPL.png'],
                        ['_z000_t000_2_Calreticulin.png', '_z000_t000_3_GM130.png'],
                        ['_z000_t000_n2_EEA1.png', '_z000_t000_3_APPL.png'],
                        ['_z000_t000_n2_EEA1.png', '_z000_t000_3_GM130.png'],
                        ['_z000_t000_3_APPL.png', '_z000_t000_3_GM130.png'],
                        ]

input_ind = int(sys.argv[1])

curr_stain_combo = staining_combination[input_ind]

for currWell in ['E11', 'F11']:
    metadata_filename = '/data/homes/jluethi/SLP_feature_values/20180601-SLP_Multiplexing_p1_' + currWell + '_Cells_metadata.csv'
    # metadata = load_tm_metadata(metadata_filename)

    calculate_correlation_for_wells(well=currWell,
                base_path='/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/illumCorr_images/',
                base_name='20180601-SLP_Multiplexing_p1_', img1_suffix=curr_stain_combo[0], img2_suffix=curr_stain_combo[1],
                segmentation_base_path = "/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/segmentations_Cells",
                segmentation_base_name = "20180601-SLP_MultiplexingSegmentation_Cells_plate_p1_well_",
                save_as_csv=True, background_threshold = 115, metadata_filename = metadata_filename)
