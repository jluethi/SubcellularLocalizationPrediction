# Script to generate padded single cell images of cells in a metadata file
import pandas as pd
import png   # pypng
import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import os
import csv

# Static variables
segmentation_path = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/segmentations_Cells/'
segmentation_prefix = '20180601-SLP_MultiplexingSegmentation_Cells_plate_'
plate_name = 'p1'
z_plane = '0'.zfill(3)
timepoint = '0'.zfill(3)
output_path = '/Users/Joel/Desktop/ExampleOutput/'
output_prefix = 'SingleCell_NUP_FollowUp1_60x'

# Helper functions


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def load_tm_metadata(metadata_filepath):
    metadata = pd.read_csv(metadata_filepath, header=0)
    total_cells = len(metadata)
    # Delete cells that are classified as 1 by any of the classifiers and remove the classifiers from the data frame
    metadata = metadata[(metadata.is_border == 0) & (metadata.DAPI_Debris == 0) &
                        (metadata.Mitotic == 0) & (metadata.Multinuclei == 0)]

    print "Discarding " + str(total_cells - len(metadata)) + ' of ' + str(
        total_cells) + ' cells, because of classifiers'

    del metadata['is_border']
    del metadata['DAPI_Debris']
    del metadata['Mitotic']
    del metadata['Multinuclei']
    return metadata


def calculate_dimensions(label, segment_data):
    # Extract the part of the image corresponding to the label
    single_cell_mask = segment_data == label

    # Find the bounding box of each single cell
    # https://stackoverflow.com/questions/31400769/bounding-box-of-numpy-array
    rows = np.any(single_cell_mask, axis=1)
    cols = np.any(single_cell_mask, axis=0)
    # Kick out labels without corresponding cells (0 pixel objects in TissueMaps)
    if sum(rows) == 0 or sum(cols) == 0:
        return [0,0]

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    rdist = rmax - rmin
    cdist = cmax - cmin

    return [rdist, cdist]


# Load data
well_names = ['C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
              'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16',
              'E05', 'E06', 'E07', 'E08', 'F05', 'F06', 'F07', 'F08']

cell_sizes_row = [['Well', 'x_pos', 'y_pos', 'label', 'size_row']]
cell_sizes_col = [['Well', 'x_pos', 'y_pos', 'label', 'size_row']]
cell_sizes_max = [['Well', 'x_pos', 'y_pos', 'label', 'size_row']]

# Loop through all the wells
for well in well_names:
    metadata_filename = '/Users/Joel/shares/workShareJoel/SLP_feature_values/20180601-SLP_Multiplexing_p1_' + well + '_Cells_metadata.csv'
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
            segmentation_filename = os.path.join(segmentation_path,
                                                 segmentation_prefix + plate_name + '_well_' + wellname +
                                                 '_x' + xpos_string + 'y' + ypos_string + '.png')

            segment_data = mpimg.imread(segmentation_filename) * 65535  # Scale to restore label values

            # Loop through all labels
            label_list = site_of_interest.label.unique()
            for label in label_list:
                # Save image of each single cell
                [size_row, size_col] = calculate_dimensions(label, segment_data)
                cell_sizes_row.append([well, x_pos, y_pos, label, size_row])
                cell_sizes_col.append([well, x_pos, y_pos, label, size_col])
                cell_sizes_max.append([well, x_pos, y_pos, label, max(size_col, size_row)])

filename = 'CellSizes_row.csv'
with open(filename, 'wb') as f1:
    wr = csv.writer(f1)
    wr.writerows(cell_sizes_row)

filename2 = 'CellSizes_col.csv'
with open(filename2, 'wb') as f2:
    wr = csv.writer(f2)
    wr.writerows(cell_sizes_col)

filename3 = 'CellSizes_maxdim.csv'
with open(filename3, 'wb') as f3:
    wr = csv.writer(f3)
    wr.writerows(cell_sizes_max)


print('Finished')
