# Create movies of stitched images based on single visiscope files
import numpy as np
import os
import sys

import imageio
import cv2

import bioformats as bf
import javabridge as jv

jv.start_vm(class_path=bf.JARS, max_heap_size='4G')

def load_downsampled_img(directory, file_prefix, channel, site, timepoint, downsample_factor):
    fname = os.path.join(directory, file_prefix + '_' + channel + '_s' + str(site) + '_t' + str(timepoint) + '.stk')
    print(fname)
    #img = cv2.imread(fname, -1)
    bf_reader = bf.ImageReader(fname, perform_init= True)
    # TODO: Option to use MIP? Load multiple z levels and project
    z_level = 1
    #z_level = 0
    img = bf_reader.read(z = z_level, t=0, rescale=False)
    new_size = (int(img.shape[0]/downsample_factor), int(img.shape[1]/downsample_factor))
    downsampled = cv2.resize(img, new_size)  # interpolation=cv2.INTER_NEAREST
    bf.clear_image_reader_cache()
    return downsampled


def stitch_img_stack(path, img_prefix, output_name, cols, rows, channel, row_shift=0, col_shift=0,
                     well_start_index=1, nb_timepoints=120, nb_cols=7, nb_rows=7,
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
    for i in range(1, nb_files+1):
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
                        if (nb_rows % 2 == 0):
                            current_site = (row + row_shift)*nb_cols + (nb_cols - (col + col_shift) - 1) + well_start_index
                        # Trying to make it work for imaging with uneven number of rows
                        else:
                            current_site = (row + row_shift)*nb_cols + (col + col_shift) + well_start_index
                    final_img[tp_relative,
                              int(row*input_img_dim[0]/downsample_factor):int((row+1)*input_img_dim[0]/downsample_factor),
                              int(col*input_img_dim[1]/downsample_factor):int((col+1)*input_img_dim[1]/downsample_factor),
                             ] = load_downsampled_img(path, img_prefix, channel, current_site, tp+1, downsample_factor)

        imageio.volwrite(output_name + '_part' + str(i) + '.tif', final_img.astype(np.uint16))

#channels = ['w3Brightfield', 'w2SolaGFP', 'w1SolaCy5']
# wells is a list of tuples. Each tuple is a well name and the well_start_index for that well and the channel to process
# Unsure about exact well order. Especially: Well D03 vs. D04
wells = [('B02', 1, 'w3Brightfield'), ('B02', 1, 'w2SolaGFP'), ('B02', 1, 'w1SolaCy5'),
         ('B03', 50, 'w3Brightfield'), ('B03', 50, 'w2SolaGFP'), ('B03', 50, 'w1SolaCy5'),
         ('C04', 99, 'w3Brightfield'), ('C04', 99, 'w2SolaGFP'), ('C04', 99, 'w1SolaCy5'),
         ('D03', 148, 'w3Brightfield'), ('D03', 148, 'w2SolaGFP'), ('D03', 148, 'w1SolaCy5'),
         ('D04', 197, 'w3Brightfield'), ('D04', 197, 'w2SolaGFP'), ('D04', 197, 'w1SolaCy5'),
         ('E03', 246, 'w3Brightfield'),  ('E03', 246, 'w2SolaGFP'),  ('E03', 246, 'w1SolaCy5'),
         ('F03', 295, 'w3Brightfield'), ('F03', 295, 'w2SolaGFP'), ('F03', 295, 'w1SolaCy5'), ]

output_basepath = '/data/active/jluethi/20211007_CardiomyocyteDifferentiation18_LiveImaging/stacks/'

# Each element is the part is: [Name of the part, nb_timepoints, number after part name]
# parts = [['part1', 20, '2'], ['part2', 26, '1'], ['part3', 22, '1'],
#          ['part4', 27, '1'], ['part5', 1, '1'], ['part6', 2, '1'], ['part7', 19, '1'], ]
parts = [['part8', 24, '1'], ['part9', 14, '1']]

job_list = []
for well in wells:
    for part in parts:
        job_list.append((well, part))

index = int(sys.argv[1])
job = job_list[index]
well = job[0]
#well = wells[index]
channel_name = well[2]
part = job[1]


#for part in parts:
print('Processing {}'.format(part[0]))
total_timepoints = part[1]
folder_path = '/data/active/jluethi/20211007_CardiomyocyteDifferentiation18_LiveImaging/{}/'.format(part[0])
prefix = '20211006_CardiomyocyteDiff18_{}{}'.format(part[0], part[2])

#for channel_name in channels:
print(well, channel_name)
#filename = '20211006_CardiomyocyteDiff18_part12_{}_'.format(part[0]) + channel_name + '_' + well[0] + '_4xDownsampled_z0'
filename = '20211006_CardiomyocyteDiff18_part12_{}_'.format(part[0]) + channel_name + '_' + well[0] + '_4xDownsampled'
output_path = os.path.join(output_basepath, filename)
stitch_img_stack(folder_path, prefix, output_path, 7, 7, channel_name, row_shift=0, col_shift=0,
                 well_start_index=well[1], nb_timepoints=total_timepoints, nb_cols=7, nb_rows=7,
                 input_img_dim=(2048, 2048), downsample_factor=4, max_timepoints_per_file=30)

print('Done! Processed {}, {}'.format(well, channel_name))
jv.kill_vm()
# TODO: end the script once it's through
sys.exit()
