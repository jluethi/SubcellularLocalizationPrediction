# Script to divide the dataset into train, validation, testing
# Get a list of all DAPI files, use them as a template for all filenames
import os
import shutil
import random
import glob
import re

percentage_train = 0.7
percentage_val = 0.15
percentage_test = 0.15

input_dir = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/singleCellImages/'
output_dir = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/singleCellImages_dividedDatasets/'

channel_names = ['10_Paxillin', '10_Pericentrin', '11_EEA1', '11_Sara', '13_DCP1a',
                 '13_DDX6', '13_Pbody_Segm', '13_Succs', '1_Lamp1', '1_PCNA',
                 '2_Calreticulin', '2_DAPI', '3_APPL', '3_GM130', '4_HSP60',
                 '4_LC3B', '5_pS6', '5_Yap', '7_Acetyl_Tubulin', '7_Actin',
                 '8_Caveolin', '8_Pol2', '9_ABCD3']

regex = '20180606-SLP_Multiplexing_p1_*DAPI*'

# get a list of all files
list_of_inputs = glob.glob(os.path.join(input_dir,regex))

print(len(list_of_inputs))

nb_inputs = len(list_of_inputs)


remaining_files = range(nb_inputs)

nb_controls = int(percentage_train * nb_inputs)
nb_val = int(percentage_val * nb_inputs)

train_indices = random.sample(remaining_files, nb_controls)


# Make target directories
os.mkdir(os.path.join(output_dir,'train'))
os.mkdir(os.path.join(output_dir,'validation'))
os.mkdir(os.path.join(output_dir,'test'))

print('Copying training files')
counter = 0
# Copy train images into target folder
for index in train_indices:
    for channel_name in channel_names:
        shutil.copy(os.path.join(input_dir, re.sub('2_DAPI',channel_name,list_of_inputs[index])), os.path.join(output_dir, 'train'))
    counter += 1
    if counter % 1000 == 0:
        print(str(counter) + ': ' + list_of_inputs[index])


# Remove train images from list
remaining_files = [x for x in remaining_files if x not in train_indices]

val_indices = random.sample(remaining_files, nb_val)

print('Copying validation files')
counter = 0
# Copy val images into target folder
for index in val_indices:
    for channel_name in channel_names:
        shutil.copy(os.path.join(input_dir, re.sub('2_DAPI',channel_name,list_of_inputs[index])), os.path.join(output_dir, 'validation'))
    counter += 1
    if counter % 1000 == 0:
        print(str(counter) + ': ' + list_of_inputs[index])

# Remove val images from list
remaining_files = [x for x in remaining_files if x not in val_indices]

print('Copying test files')
counter = 0
# Copy test images into target folder
for index in remaining_files:
    for channel_name in channel_names:
        shutil.copy(os.path.join(input_dir, re.sub('2_DAPI',channel_name,list_of_inputs[index])), os.path.join(output_dir, 'test'))
    counter += 1
    if counter % 1000 == 0:
        print(str(counter) + ': ' + list_of_inputs[index])


