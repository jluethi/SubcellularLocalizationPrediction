# Script to rename ilastik probability maps into an additional channel of CV7K images
import os
import re
import shutil

channel = 'C05'
input_dir = '/Users/Joel/shares/dataShareJoel/jluethi/20180730_bDNA-FISH_Pbodies/images/'
output_dir = '/Users/Joel/shares/dataShareJoel/jluethi/20180730_bDNA-FISH_Pbodies/images/'
file_ending = 'Probabilities.png'

file_list_tmp = os.listdir(input_dir)
file_list = []

for fyle in file_list_tmp:
    if fyle.endswith(file_ending):
        file_list.append(fyle)

print(len(file_list))


for counter, fyle in enumerate(file_list):
    if counter % 100 == 0:
        print(counter)


    output_filename = fyle[:-21] + channel + '.png'

    input_file_path = os.path.join(input_dir, fyle)
    destination_filename_new = os.path.join(output_dir, output_filename)
    shutil.copyfile(input_file_path, destination_filename_new)

