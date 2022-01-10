# Convert visiscope stacks of 20190403-WTC_PermeabilizationTest experiment to projected pngs
import bioformats as bf
import javabridge as jv
import numpy as np
import cv2
import os
import sys

print('Starting')

jv.start_vm(class_path=bf.JARS, max_heap_size='1G')

def stk_to_cv7k_png(input_path, output_path, prefix, channels, well, site, nb_sites_per_well, z_steps, project = False):
    channel_numbers = ['01', '02', '03', '04']
    for curr_channel_number in range(len(channels)):
        filename = os.path.join(input_path, prefix + '_'+ channels[curr_channel_number] + '_s' + str(site) + '.stk')
        bf_reader = bf.ImageReader(filename, perform_init= True)
        # md = bf.get_omexml_metadata(filename)
        # print(xml_pretty.parseString(md.encode('utf-8')).toprettyxml())

        # Load all z dims, then project
        size = [z_steps,2048, 2048]
        # Map the increasing site numbers back to site numbers per well
        new_site = (site - 1) % nb_sites_per_well + 1
        if project == True:
            img = np.empty(size, np.uint16)

            output_filename = prefix + '_' + well + '_' + 'T001F' + str(new_site).zfill(3) + 'L01A01Z01C' + channel_numbers[
                curr_channel_number] + '.png'

            for i in range(z_steps):
                img[i] = bf_reader.read(z = i, t=0, rescale=False)
            projected_img = img.max(axis=0)


            cv2.imwrite(os.path.join(output_path,  output_filename), projected_img)

        if project == False:
            i = 9
            output_filename = prefix + '_' + well + '_' + 'T001F' + str(new_site).zfill(3) + 'L01A01Z' + str(i+1).zfill(2) + \
                              'C' + channel_numbers[curr_channel_number] + '.png'
            img = bf_reader.read(z=i, t=0, rescale=False)

            cv2.imwrite(os.path.join(output_path, output_filename), img)


prefix = '20190415-WTC-PermeabilizationTest1-CollagenStaining1'
# channels = ['w1sdcDAPIxmRFPm', 'w2sdcGFP-Cam1', 'w3sdcRFP590-20', 'w4sdcCy5']
channels = ['w1sdcDAPIxmRFPm', 'w2sdcRFP590-20']
z_steps = 18
output_path = '/data/active/jluethi/20190415-WTC-PermeabilizationTest1-CollagenStaining/projected_pngs/'
input_path = '/data/active/jluethi/20190415-WTC-PermeabilizationTest1-CollagenStaining/visiscope_stacks/'

# wells = [[list(range(1, 37)), 'B02'], [list(range(37, 73)), 'B03'], [list(range(73, 109)), 'B04'], [list(range(109, 145)), 'B05'],
#          [list(range(145, 181)), 'C05'], [list(range(181, 217)), 'C04'], [list(range(217, 253)), 'C03'], [list(range(253, 289)), 'C02'],
#          [list(range(289, 325)), 'D02'], [list(range(325, 361)), 'D03'], [list(range(361, 397)), 'D04'], [list(range(397, 433)), 'D05'],
#          [list(range(433, 469)), 'E05'], [list(range(469, 505)), 'E04'], [list(range(505, 541)), 'E03'], [list(range(541, 577)), 'F03'], [list(range(577, 613)), 'F05']]
wells = [[list(range(1, 37)), 'B02'], [list(range(37, 73)), 'B03'], [list(range(73, 109)), 'B04'], [list(range(109, 145)), 'B05']]
nb_sites_per_well = 36

# for curr_well in wells:
index = int(sys.argv[1])
curr_well = wells[index]
well = curr_well[1]
for site in curr_well[0]:
    print('Processing site ' + str(site))
    stk_to_cv7k_png(input_path, output_path, prefix, channels, well, site, nb_sites_per_well, z_steps, project = True)

jv.kill_vm()
print('Finished')
