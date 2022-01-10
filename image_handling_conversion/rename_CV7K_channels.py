# Script to change the channel names of CV7K images
import os
import shutil

# from A03Z01C04.png
# to A01Z01C02.png

channel = 'A01Z01C02'
input_dir = '/Users/Joel/shares/dataShareJoel/jluethi/20190429-WTC-PermeabilizationTest4/red_images/'
output_dir = '/Users/Joel/shares/dataShareJoel/jluethi/20190429-WTC-PermeabilizationTest4/images/'
file_ending = 'A03Z01C04.png'

file_list_tmp = os.listdir(input_dir)
file_list = []

for fyle in file_list_tmp:
    if fyle.endswith(file_ending):
        file_list.append(fyle)

print(len(file_list))


for counter, fyle in enumerate(file_list):
    if counter % 100 == 0:
        print(counter)


    output_filename = fyle[:-13] + channel + '.png'

    input_file_path = os.path.join(input_dir, fyle)
    destination_filename_new = os.path.join(output_dir, output_filename)
    shutil.copyfile(input_file_path, destination_filename_new)
