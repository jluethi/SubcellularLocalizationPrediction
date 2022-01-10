# Script to generate padded single cell images of cells in a metadata file
import pandas as pd
import png   # pypng
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import os
import sys
import csv

# Static variables
# image_path = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/illumCorr_images'
image_name_prefix = '20180601-SLP_Multiplexing'
# segmentation_path = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/segmentations_Cells/'
segmentation_prefix = '20180601-SLP_MultiplexingSegmentation_Cells_plate_'
channel_suffixes = ['13_Pbody_Segm']
plate_name = 'p1'
z_plane = '0'.zfill(3)
timepoint = '0'.zfill(3)
output_prefix = '20180606-SLP_Multiplexing'
# metadata_path = '/data/homes/jluethi/SLP_feature_values/'
metadata_prefix = '20180601-SLP_Multiplexing_p1_'
background_level = 0
background_std = 0
image_size = 640

# tmp variables
image_path = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/illumCorr_images'
segmentation_path = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/segmentations_Cells/'
metadata_path = '/Users/Joel/shares/workShareJoel/SLP_feature_values/'
output_path = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/'



# Helper functions

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def create_vector_gaussian_noise(size, mean, std):
    return np.random.normal(loc = mean, scale = std, size = size)


def add_background_padding(vector, iaxis_pad_width, iaxis, kwargs):
    vector[:iaxis_pad_width[0]] = create_vector_gaussian_noise(iaxis_pad_width[0],
                                                               background_level, std = background_std)
    vector[-iaxis_pad_width[1]:] = create_vector_gaussian_noise(iaxis_pad_width[1],
                                                                background_level, std = background_std)
    return vector


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


def export_single_cell(label, segment_data, imageData, image_size):
    # Extract the part of the image corresponding to the label
    single_cell_mask = segment_data == label

    # Find the bounding box of each single cell
    # https://stackoverflow.com/questions/31400769/bounding-box-of-numpy-array
    rows = np.any(single_cell_mask, axis=1)
    cols = np.any(single_cell_mask, axis=0)
    # Kick out labels without corresponding cells (0 pixel objects in TissueMaps, tiny objects)
    if sum(rows) < 10 or sum(cols) < 10:
        return []

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    rdist = rmax - rmin
    cdist = cmax - cmin

    single_cell_image = imageData[rmin:rmax, cmin:cmax]
    single_cell_segmentation = single_cell_mask[rmin:rmax, cmin:cmax]

    max_dim = max(rdist, cdist)
    # Currently, add_background_padding breaks when no padding is applied.
    # Therefore, the input size is considered too large if it is bigger than image_size - 2
    if max_dim > (image_size - 2):
        return []

    else:
        single_cell_image_cleanedUp = np.zeros(single_cell_image.shape) + \
                                      np.multiply(single_cell_image, single_cell_segmentation) * 65535 + \
                                      np.multiply(create_vector_gaussian_noise(size= single_cell_image.shape,
                                                mean=background_level, std=background_std),
                                                np.logical_not(single_cell_segmentation))

        # plt.imshow(single_cell_image_cleanedUp)
        # plt.show()

        # Pad image on all sides to make it of the image_size
        lower_r_dist = int((image_size - rdist) / 2)
        upper_r_dist = int(math.ceil((image_size - rdist) / 2.))
        lower_c_dist = int((image_size - cdist) / 2)
        upper_c_dist = int(math.ceil((image_size - cdist) / 2.))
        padded_image = np.pad(single_cell_image_cleanedUp, pad_width=((lower_r_dist, upper_r_dist),
                                                                      (lower_c_dist, upper_c_dist)),
                              mode=add_background_padding)


        # Calculate the area of P bodies & area of background for the cell
        rescaled_img = (padded_image > 32767)
        pbody_pixels = np.sum(rescaled_img)
        total_area = np.sum(single_cell_segmentation)
        background_pixels = total_area - pbody_pixels
        percentage_pbody = float(pbody_pixels) / total_area

        return [pbody_pixels, background_pixels, total_area, percentage_pbody]


# Load data
well_names = ['C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
              'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16',
              'E05', 'E06', 'E07', 'E08', 'F05', 'F06', 'F07', 'F08']

csv_output_name = os.path.join(output_path, 'Pbody_Sizes.csv')

well_info = ['Well']
sitex = ['SiteX']
sitey = ['SiteY']
label_info = ['Label']
pbody_areas = ['PbodyArea']
background_areas = ['BackgroundArea']
total_areas = ['TotalArea']
percentages_pbodies = ['PercentagePbody']
area_data = []

# Loop through all the wells
# index = int(sys.argv[1])
for index in range(len(well_names)):
    well = well_names[index]
    print('Processing well ' + well)

    metadata_filename = os.path.join(metadata_path, metadata_prefix + well + '_Cells_metadata.csv')
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

            print "Processing:", well, "x", str(x_pos), 'y', str(y_pos)

            # Make filenames
            xpos_string = str(site_of_interest['well_pos_x'].iloc[0])
            ypos_string = str(site_of_interest['well_pos_y'].iloc[0])
            wellname = site_of_interest['well_name'].iloc[0]
            segmentation_filename = os.path.join(segmentation_path, segmentation_prefix + plate_name + '_well_' + wellname + \
                                    '_x' + xpos_string +'y' + ypos_string + '.png')

            # Load channel image and segmentation image
            segment_data = mpimg.imread(segmentation_filename) * 65535  # Scale to restore label values

            # Loop through all the image channels
            for channel_idx, channel_suffix in enumerate(channel_suffixes):
                image_file_name = os.path.join(image_path, image_name_prefix + '_' + plate_name + '_' + wellname + '_y'
                                               + ypos_string.zfill(3) + '_x' + xpos_string.zfill(3) + '_z' + z_plane +
                                               '_t' + timepoint + '_' + channel_suffix + '.png')

                imageData = mpimg.imread(image_file_name)

                # Show image
                # imgplot = plt.imshow(segment_data)
                # plt.show()

                # Loop through all labels
                label_list = site_of_interest.label.unique()
                for label in label_list:
                    # Save image of each single cell
                    areas = export_single_cell(label, segment_data, imageData, image_size)
                    if len(areas) > 1:
                        pbody_areas.append(areas[0])
                        background_areas.append(areas[1])
                        total_areas.append(areas[2])
                        percentages_pbodies.append(areas[3])
                        well_info.append(well)
                        sitex.append(x_pos)
                        sitey.append(y_pos)
                        label_info.append(label)

area_data = zip(well_info, sitex, sitey, label_info, pbody_areas, background_areas, total_areas, percentages_pbodies)

with open(csv_output_name, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(area_data)



