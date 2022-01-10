# Script to rename ilastik probability maps into an additional channel of CV7K images
import os
import re
import shutil

channel_list = ['', 'C01', 'C02', 'C03', 'C02']
action_number = 'A01'
input_base = '/data/active/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/MIPs/'
'20190917-Cardiomyocyte-Multiplexing_Differentiated_p1_F06_y011_x008_z000_t000_1_A02_C03.png'
nb_cols = 9
output_base = '/data/active/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/MIPs_renamed/'

cycles = ['Cycle1', 'Cycle2', 'Cycle4', 'Cycle5', 'Cycle6', 'Cycle7', 'Cycle11']


for cycle in cycles:
    input_dir = os.path.join(input_base, cycle)
    output_dir = os.path.join(output_base, cycle)
    file_list = os.listdir(input_dir)
    for counter, fyle in enumerate(file_list):
        if counter % 100 == 0:
            print(counter)

        well = re.findall('\w\d\d_y', fyle)[0][:3]
        ypos = int(re.findall('_y\d\d\d_', fyle)[0][2:-1])
        xpos = int(re.findall('_x\d\d\d_', fyle)[0][2:-1])
        site = nb_cols * ypos + xpos + 1
        input_channel = int(re.findall('C\d\d.png', fyle)[0][1:3])

        output_filename = '20190929_CardiomyocyteDifferentiation_' + well + '_T0003F' + str(site).zfill(3) + \
                          'L01' + action_number + 'Z01' + channel_list[input_channel] + '.png'

        input_file_path = os.path.join(input_dir, fyle)
        destination_filename_new = os.path.join(output_dir, output_filename)
        shutil.copyfile(input_file_path, destination_filename_new)

