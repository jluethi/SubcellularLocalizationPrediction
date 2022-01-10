# Script to divide the dataset into train, validation, testing
# Get a list of all DAPI files, use them as a template for all filenames
import os
import shutil
import random
import glob
import re

target_dir = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/singleCellImages_dividedDatasets/'
subdirs = ['train/', 'validation/', 'test/']
input_dir = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/singleCellSegmentations/'

regex = '20180606-SLP_Multiplexing_p1_*DAPI*'

for subdir in subdirs:
    output_dir = os.path.join(target_dir, subdir)

    # get a list of all files
    list_of_inputs = glob.glob(os.path.join(output_dir, regex))

    print('Copying '+ subdir +' files: ' + str(len(list_of_inputs)))

    counter = 0
    # Copy train images into target folder
    for index in range(len(list_of_inputs)):
        new_filename = re.sub('2_DAPI','segmentation',list_of_inputs[index]).split('/')[-1]

        shutil.copy(os.path.join(input_dir, new_filename), output_dir)
        counter += 1
        if counter % 1000 == 0:
            print(str(counter) + ': ' + list_of_inputs[index])

