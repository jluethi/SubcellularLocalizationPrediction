# Script to rename ilastik probability maps into an additional channel of CV7K images
import os
import re
import shutil

channel = 'C04'
action_number = 'A04'
input_dir = '/Users/Joel/shares/workShareJoel/20180523_SLP_DDX6_Segmentation_v2'
nb_cols = 6
output_dir = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/Cycle13_PNG/MainExperiment'

file_list = os.listdir(input_dir)

print(len(file_list))


for counter, fyle in enumerate(file_list):
    if counter % 100 == 0:
        print(counter)

    well = re.findall('\w\d\d_y', fyle)[0][:3]
    ypos = int(re.findall('_y\d\d\d_', fyle)[0][2:-1])
    xpos = int(re.findall('_x\d\d\d_', fyle)[0][2:-1])
    site = nb_cols * ypos + xpos + 1

    output_filename = 'AssayPlate_Greiner_781091_' + well + '_T0003F' + str(site).zfill(3) + 'L01' + action_number + 'Z01' + channel + '.png'

    input_file_path = os.path.join(input_dir, fyle)
    destination_filename_new = os.path.join(output_dir, output_filename)
    shutil.copyfile(input_file_path, destination_filename_new)

