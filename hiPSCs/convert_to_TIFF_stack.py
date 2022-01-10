# Script to convert CV7K TIFFs or PNGs to TIFF stacks
import os
import re
import numpy as np
from pathlib import Path
# import pandas as pd
import imageio
import sys


def manage_stack_conversion(input_path, output_path, wells_to_process=None, sites_to_process=None,
                            dim_y=2160, dim_x=2560, shifts=None):
    """Converts all the Z images of the CV7K to a Z-Stack TIFF image

     Args:
         input_path (Path or str): Path to the input files
         output_path (Path or str): Path to the output directory
         wells_to_process (None or list): List of wells to be processed. If none, process all files in the input folder
         sites_to_process (None or list): Optionally specify a list of sites that should be processed for each well
         dim_y (int): Dimension of images in y direction
         dim_x (int): Dimension of images in x direction
         shifts (None or list): list of shift parameters to shift the resulting stack. If nothing is provided, the
            stack is not shifted. List contains: max_shift_x, min_shift_x, current_shift_x, max_shift_y, min_shift_y,
            current_shift_y

     """

    input_path = Path(input_path)
    output_path = Path(output_path)

    # List all files in the folder
    files = os.listdir(str(input_path))

    regex_wells = re.compile('.*_(?P<Well>[A-Z]\\d{2})_T\\d+F\\d+L\\d+A\\d+Z\\d+C\\d+.*')
    wells = set()

    # Find all the wells in the experiment
    for fyle in files:
        file_metadata = regex_wells.match(fyle)
        if file_metadata:
            wells.add(file_metadata.group(1))

    # If wells_to_process specifies a list of wells, only process those wells
    if wells_to_process:
        wells = wells & set(wells_to_process)

    # Loop through the wells
    for well in wells:
        sites = set()
        # Create set of all sites
        regex_sites = re.compile('.*_' + well + '_T\\d+F(?P<Site>\\d+)L\\d+A\\d+Z(?P<Zlevel>\\d+)C(?P<Channel>\\d+).*')
        for fyle in files:
            file_metadata = regex_sites.match(fyle)
            if file_metadata:
                sites.add(int(file_metadata.group(1)))

        # If a list of sites to be processed is specified,
        if sites_to_process:
            sites = sites & set(sites_to_process)

        # Loop through all sites
        for curr_site in sites:
            print(curr_site)
            # Check all channels
            channels = set()
            regex_channels = re.compile('.*_' + well + '_T\\d+F' + str(curr_site).zfill(3) +
                                        'L\\d+A\\d+Z(?P<Zlevel>\\d+)(?P<Channel>C\\d+).*')
            for fyle in files:
                file_metadata = regex_channels.match(fyle)
                if file_metadata:
                    channels.add(file_metadata.group(2))

            # Loop through each channel and find all the sites
            for curr_channel in channels:
                convert_cv7k_images_to_stack(input_path, output_path, well, curr_site, curr_channel, dim_y=dim_y,
                                             dim_x=dim_x, shifts=shifts)


def convert_cv7k_images_to_stack(input_path, output_path, well, curr_site, curr_channel,
                                 dim_y=2160, dim_x=2560, shifts=None):
    """Converts all the Z images of the CV7K to a Z-Stack TIFF image

     Args:
         input_path (Path or str): Path to the input files
         output_path (Path or str): Path to the output directory
         well (str): Current well to be processed
         curr_site (int): Current site to be processed
         curr_channel (str): Current channel to be processed
         dim_y (int): Dimension of images in y direction
         dim_x (int): Dimension of images in x direction
         shifts (None or list): list of shift parameters to shift the resulting stack. If nothing is provided, the
            stack is not shifted. List contains: max_shift_x, min_shift_x, current_shift_x, max_shift_y, min_shift_y,
            current_shift_y

     """
    # List all files in the folder
    files = os.listdir(str(input_path))

    z_levels = list()
    regex_z = re.compile('.*_' + well + '_T\\d+F' + str(curr_site).zfill(3) +
                         'L\\d+A\\d+Z(?P<Zlevel>\\d+)' + curr_channel + '.*')
    for fyle in files:
        file_metadata = regex_z.match(fyle)
        if file_metadata:
            z_levels.append(int(file_metadata.group(1)))

    nb_z_steps = max(z_levels)

    # Assert that all Z positions are available (len == max value),
    # e.g. there are no Z positions missing in the middle
    assert len(z_levels) == nb_z_steps, 'Z levels are missing for ' + well + ': Site ' + \
                                        str(curr_site) + ' ' + curr_channel

    curr_stack = np.zeros((nb_z_steps, dim_y, dim_x)).astype('uint16')

    for curr_z in range(1, nb_z_steps + 1):
        regex_file = re.compile('.*_' + well + '_T\\d+F' + str(curr_site).zfill(3) + 'L\\d+A\\d+Z' +
                                str(curr_z).zfill(2) + curr_channel + '.*')

        curr_file = list(filter(regex_file.match, files))[0]
        curr_stack[curr_z - 1, :, :] = imageio.imread(folder_path / curr_file)

    regex_file = re.compile('.*_' + well + '_T\\d+F' + str(curr_site).zfill(3) + 'L\\d+A\\d+Z' +
                            str(1).zfill(2) + curr_channel + '.*')
    curr_file = list(filter(regex_file.match, files))[0]
    output_filename = 'Stack_' + curr_file.split('.')[0] + '.tif'

    # cut curr_stack to align it according to input parameters
    if shifts:
        shifted_stack = curr_stack[:, (shifts[3] - shifts[5]):(dim_y + shifts[4] - shifts[5]),
                                   (shifts[0] - shifts[2]):(dim_x + shifts[1] - shifts[2])]
        imageio.volwrite(output_path / output_filename, shifted_stack)
    else:
        imageio.volwrite(output_path / output_filename, curr_stack)


### Template for input when not using any cycle specific shifts
# wells = ['C02', 'D02', 'F02', 'G02', 'C04', 'D04', 'F04', 'G04', 'C06', 'D06', 'F06', 'G06', 'C08', 'D08', 'F08',
#         'G08', 'F10', 'G10']
# index = int(sys.argv[1])
# well_name = wells[index]
# cycles = ['Cycle1', 'Cycle2', 'Cycle3', 'Cycle4', 'Cycle5', 'Cycle6', 'Cycle7', 'Cycle11']

# cycles = ['Cycle1']

# for i, cycle in enumerate(cycles):
#     well_name = 'F06'
#     sites_processing = [23]
#     # sites_processing = list(range(1, 11))
#     folder_path = Path('/Users/Joel/shares/dataShareJoel/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/' + cycle + '/image_links/' + 'differentiated/')
#     # target_path = Path('/Users/Joel/shares/workShareJoel/20190923_SitesOfInterest/Stacks')
#     target_path = Path('/Users/Joel/Desktop')
#
#     manage_stack_conversion(folder_path, target_path, wells_to_process=[well_name],
#                             sites_to_process=sites_processing)

# wells_list = ['B04', 'B05', 'C05']
# for well_name in wells_list:
#     sites_processing = list(range(1, 82))
#     folder_path = Path('/data/active/jluethi/20191031-Joel-WTCStainingTest4/3D-60x/images')
#     target_path = Path('/data/active/jluethi/20191031-Joel-WTCStainingTest4/3D-60x/stacks')
#
#     manage_stack_conversion(folder_path, target_path, wells_to_process=[well_name],
#                             sites_to_process=sites_processing)


# sites_processing = list(range(1, 144))
# folder_path = Path('/data/active/jluethi/20191206-CAAX-gfp/40x-images')
# target_path = Path('/data/active/jluethi/20191206-CAAX-gfp/40x-stacks')
#
# manage_stack_conversion(folder_path, target_path)


# sites_processing = list(range(1, 211))

folder_path = Path('/data/active/jluethi/20200228-CardiomyocyteDifferentiation8/3D')
target_path = Path('/data/active/jluethi/20200228-CardiomyocyteDifferentiation8/stacks')
sites_processing = list(range(1, 5))

manage_stack_conversion(folder_path, target_path, sites_to_process=sites_processing)


### Template for Z-stack creation with shift correction
# Site is a list of lists. Each sublist contains: Name of the well (string), list of sites to be processed
# [list of int], name of the subfolder containing images of this site, list of y_shifts for the different cycles,
# list of x_shifts for the different cycles
# sites = [['D02', [79], 'undifferentiated/', [0, 15, -2, 48, 50, 33, 49, 41], [0, 16, -21, -22, -39, -78, -62, -73]]]
# sites = [['F02', [25], 'start_differentiation/', [0, 21,1,52,57,39,60,51], [0, 14, -30,-24,-44,-72,-72,-73]],
#          ['D04', [59], 'start_differentiation/', [0,13,3,47,54,25,44,42], [0,19,-18,-24,-37,-74,-73,-69]],
#          ['F04', [22], 'start_differentiation/', [0,20,7,51,58,32,52,48], [0,14,-26,-21,-38,-66,-66,-71]],
#          ['D06', [52], 'differentiated/', [0,13,10,47,54,17,40,41], [0,16,-15,-19,-34,-70,-68,-64]],
# sites = [['F06', [23], 'differentiated/', [0,18,11,52,58,24,45,46], [0,18,-19,-19, -35,-60,-63,-64]],
#          ['D06', [52], 'differentiated/', [0,13,10,47,54,17,40,41], [0,16,-15,-19,-34,-70,-68,-64]]]
# sites = [['F06', [23], 'differentiated/', [0,18,11,52,58,24,45,46], [0,18,-19,-19, -35,-60,-63,-64]]]
#
# # cycles = ['Cycle1', 'Cycle2', 'Cycle3', 'Cycle4', 'Cycle5', 'Cycle6', 'Cycle7', 'Cycle11']
# cycles = ['Cycle1']
#
# for site in sites:
#     shifts_y = site[3]
#     shifts_x = site[4]
#     for i, cycle in enumerate(cycles):
#         well_name = site[0]
#         sites_processing = site[1]
#         folder_path = Path('/Users/Joel/shares/dataShareJoel/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/' + cycle + '/image_links/' + site[2])
#         # target_path = Path('/Users/Joel/shares/workShareJoel/20190923_SitesOfInterest/Stacks')
#         target_path = Path('/Users/Joel/Desktop')
#
#         # calculate shift statistics:
#         max_x_shift = max(shifts_x)
#         min_x_shift = min(shifts_x)
#         curr_x_shift = shifts_x[i]
#
#         max_y_shift = max(shifts_y)
#         min_y_shift = min(shifts_y)
#         curr_y_shift = shifts_y[i]
#
#         shift_params = [max_x_shift, min_x_shift, curr_x_shift, max_y_shift, min_y_shift, curr_y_shift]
#
#         manage_stack_conversion(folder_path, target_path, wells_to_process=[well_name],
#                                 sites_to_process=sites_processing, shifts=shift_params)
