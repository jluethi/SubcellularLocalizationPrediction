# Script to generate padded single cell images of cells in a metadata file
import pandas as pd
import png   # pypng
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import os

# Static variables
segmentation_path = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/segmentations_Cells/'
segmentation_prefix = '20180601-SLP_MultiplexingSegmentation_Cells_plate_'

plate_name = 'p1'
z_plane = '0'.zfill(3)
timepoint = '0'.zfill(3)
output_path = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/singleCellSegmentations'
output_prefix = '20180606-SLP_Multiplexing'
background_level = 0
background_std = 0
image_size = 640

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


def export_single_cell_segmentation(xpos_string,ypos_string, label, segment_data, image_size,timepoint, z_plane,counter_input):
    # Extract the part of the image corresponding to the label
    single_cell_mask = segment_data == label

    # Find the bounding box of each single cell
    # https://stackoverflow.com/questions/31400769/bounding-box-of-numpy-array
    rows = np.any(single_cell_mask, axis=1)
    cols = np.any(single_cell_mask, axis=0)
    # Kick out labels without corresponding cells (0 pixel objects in TissueMaps, tiny objects)
    if sum(rows) < 10 or sum(cols) < 10:
        return counter_input

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    rdist = rmax - rmin
    cdist = cmax - cmin

    single_cell_image = single_cell_mask[rmin:rmax, cmin:cmax]
    single_cell_segmentation = single_cell_mask[rmin:rmax, cmin:cmax]

    max_dim = max(rdist, cdist)
    # Currently, add_background_padding breaks when no padding is applied.
    # Therefore, the input size is considered too large if it is bigger than image_size - 2
    if max_dim > (image_size - 2):
        image_name = plate_name + '_' + wellname + '_x' + \
                     xpos_string.zfill(3) + '_y' + ypos_string.zfill(3) + '_z' + z_plane + '_t' + \
                     timepoint

        print 'Very large cell: ', max_dim, ' px, ', image_name
        return counter_input + 1


    else:
        single_cell_image_cleanedUp = np.zeros(single_cell_image.shape) + \
                                      np.multiply(single_cell_image, single_cell_segmentation) * 65535

        # Pad image on all sides to make it of the image_size
        lower_r_dist = int((image_size - rdist) / 2)
        upper_r_dist = int(math.ceil((image_size - rdist) / 2.))
        lower_c_dist = int((image_size - cdist) / 2)
        upper_c_dist = int(math.ceil((image_size - cdist) / 2.))
        padded_image = np.pad(single_cell_image_cleanedUp, pad_width=((lower_r_dist, upper_r_dist),
                                                                      (lower_c_dist, upper_c_dist)),
                              mode=add_background_padding)


        rescaled_img = padded_image * 255
        # Catch values < 0 or > 255
        rescaled_img[rescaled_img < 0] = 0
        rescaled_img[rescaled_img > 255] = 255


        output_file_name = os.path.join(output_path, output_prefix + '_' + plate_name + '_' + wellname + '_x' +
                           xpos_string.zfill(3) + '_y' + ypos_string.zfill(3) + '_z' + z_plane + '_t' +
                           timepoint + '_' + 'segmentation' + '_Label' + str(label) + '.png')

        f = open(output_file_name, 'wb')
        w = png.Writer(width=rescaled_img.shape[1], height=rescaled_img.shape[0],
                       bitdepth=8, greyscale=True)
        w.write(f, rescaled_img)
        f.close()
        return counter_input


# Load data
well_names = ['C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
              'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16',
              'E05', 'E06', 'E07', 'E08', 'F05', 'F06', 'F07', 'F08']

counter_big_cells = 0

# Loop through all the wells
for well in well_names:
    metadata_filename = '/data/homes/jluethi/SLP_feature_values/20180601-SLP_Multiplexing_p1_' + well + '_Cells_metadata.csv'
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

            # Loop through all labels
            label_list = site_of_interest.label.unique()
            for label in label_list:
                # Save image of each single cell
                counter_big_cells = export_single_cell_segmentation(xpos_string, ypos_string,
                                                       label, segment_data, image_size, timepoint,
                                                       z_plane, counter_big_cells)


print(str(counter_big_cells) + ' Cells discarded, because they were bigger '
                               'than %d pixels in one dimension' % image_size)

