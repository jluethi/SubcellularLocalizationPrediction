# Create movies of stitched images based on single visiscope files
import numpy as np
import os
import sys

import imageio
import cv2
# import matplotlib.pyplot as plt


def load_downsampled_img(directory, file_prefix, channel, site, timepoint, downsample_factor):
    fname = os.path.join(directory, file_prefix + '_' + channel + '_s' + str(site) + '_t' + str(timepoint) + '.tif')
    img = cv2.imread(fname, -1)
    new_size = (int(img.shape[0]/downsample_factor), int(img.shape[1]/downsample_factor))
    downsampled = cv2.resize(img, new_size)  # interpolation=cv2.INTER_NEAREST
    return downsampled


def stitch_img_stack(path, img_prefix, output_name, cols, rows, channel, row_shift=0, col_shift=0,
                     well_start_index=1, nb_timepoints=120, nb_cols=8,
                     input_img_dim=(2048, 2048), downsample_factor=2, max_timepoints_per_file=60):
    '''
    Function stitches multiple images from the visiscope in a horizontal zick-zack fashion in x & y & time
    and saves the resulting z-stack to a TIFF file

    Known limitations: Only coded for wells in which an even number of rows was acquired.
    Otherwise, the zig-zag stitching is reversed at the moment

    '''
    # Processes only max_timepoints_per_file at a time. Saves memory and is needed
    # because imageio can't save TIFF files bigger than 60 GB
    # For saving: Save stack in parts if it contains more than max_timepoints_per_file timepoints
    nb_files = int(nb_timepoints/max_timepoints_per_file) + 1
    for i in range(1, nb_files):
        max_tp = min(nb_timepoints, i*max_timepoints_per_file)
        tps_in_cycle = max_tp - (i-1)*max_timepoints_per_file
        output_img_dim = (tps_in_cycle, int(input_img_dim[0] * rows/downsample_factor),
                          int(input_img_dim[1] * cols/downsample_factor))

        final_img = np.zeros(output_img_dim)

        for tp_relative in range(tps_in_cycle):
            tp = tp_relative + (i-1)*max_timepoints_per_file
            print('Current timepoint: ' + str(tp + 1))
            for row in range(rows):
                for col in range(cols):
                    if (row + row_shift) % 2 == 0:
                        current_site = (row + row_shift)*nb_cols + (col + col_shift) + well_start_index
                    else:
                        current_site = (row + row_shift)*nb_cols + (nb_cols - (col + col_shift) - 1) + well_start_index
                    final_img[tp_relative,
                              int(row*input_img_dim[0]/downsample_factor):int((row+1)*input_img_dim[0]/downsample_factor),
                              int(col*input_img_dim[1]/downsample_factor):int((col+1)*input_img_dim[1]/downsample_factor),
                             ] = load_downsampled_img(path, img_prefix, channel, current_site, tp+1, downsample_factor)

        imageio.volwrite(output_name + '_part' + str(i) + '.tif', final_img.astype(np.uint16))

channels = ['w1DIC1', 'w2SolaGFP']
# wells is a list of tuples. Each tuple is a well name and the well_start_index for that well
wells = [('B04', 1), ('C04', 65), ('D04', 129), ('E04', 193)]
output_basepath = '/data/active/jluethi/20191122-CardiomyocyteDifferentiation-LiveImaging/stacks/'

# Batch 1
# total_timepoints = 120
# folder_path = '/data/active/jluethi/20191122-CardiomyocyteDifferentiation-LiveImaging/images/'
# prefix = '20191122-Cardiomyocyte_LiveCellImaging_LongTerm1'

# Batch 2
total_timepoints = 168
folder_path = '/data/active/jluethi/20191122-CardiomyocyteDifferentiation-LiveImaging/images_2/'
prefix = '20191127-Cardiomyocyte_LiveCellImaging_LongTerm1'

index = int(sys.argv[1])
well = wells[index]

for channel_name in channels:
    filename = '20191122-Cardiomyocyte_LiveCellImaging_batch2_' + channel_name + '_' + well[0] + '_4xDownsampled'
    output_path = os.path.join(output_basepath, filename)
    stitch_img_stack(folder_path, prefix, output_path, 8, 8, channel_name, row_shift=0, col_shift=0,
                     well_start_index=well[1], nb_timepoints=total_timepoints, nb_cols=8,
                     input_img_dim=(2048, 2048), downsample_factor=4, max_timepoints_per_file=30)
