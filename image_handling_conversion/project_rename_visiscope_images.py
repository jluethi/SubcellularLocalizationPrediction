# Script to load visiscope stk files, project if wanted and convert them to png
import bioformats as bf
import javabridge as jv
import numpy as np
import cv2
import os
import xml.dom.minidom as xml_pretty
from matplotlib import pyplot as plt

jv.start_vm(class_path=bf.JARS, max_heap_size='4G')


def stk_to_cv7k_png(input_path, output_path, prefix, well, channels, curr_channel_number,z_steps, sites, project = True):
    channel_numbers = ['01', '02', '03', '04']

    for site in sites:
        filename = os.path.join(input_path, prefix + '-' + well + '-1_' + channels[curr_channel_number] + '_s' + str(site) + '.stk')
        # filename = os.path.join(input_path, prefix + '-' + well + '3_' + channels[curr_channel_number] + '_s' + str(site) + '.stk')
        bf_reader = bf.ImageReader(filename, perform_init= True)
        # md = bf.get_omexml_metadata(filename)
        # print(xml_pretty.parseString(md.encode('utf-8')).toprettyxml())

        # Load all z dims, then project
        size = [z_steps,2048, 2048]
        if project == True:
            img = np.empty(size, np.uint16)

            output_filename = prefix + '_' + well + '_' + 'T001F' + str(site).zfill(3) + 'L01A01Z01C' + channel_numbers[
                curr_channel_number] + '.png'

            for i in range(z_steps):
                img[i] = bf_reader.read(z = i, t=0, rescale=False)
            projected_img = img.max(axis=0)


            cv2.imwrite(os.path.join(output_path,  output_filename), projected_img)

        if project == False:
            for i in range(z_steps):
                # img = np.empty(size[1:], np.uint16)
                output_filename = prefix + '_' + well + '_' + 'T001F' + str(site).zfill(3) + 'L01A01Z0' + str(i+1) + \
                                  'C' + channel_numbers[curr_channel_number] + '.png'
                img = bf_reader.read(z=i, t=0, rescale=False)

                cv2.imwrite(os.path.join(output_path, output_filename), img)


prefix = 'R20181207-Stellaris4'
channels = ['w1sdcDAPIxmRFPm', 'w2sdcRFP590-20', 'w2sdcGFP', 'w3hxpCy5']
z_steps = 12
sites = list(range(1,26))
output_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle1-Stellaris_PNGs/'
input_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle1-Stellaris/'


wells = ['C04', 'C05', 'C06', 'D03', 'D04', 'E03', 'E04'] #, 'E05', 'E06', 'F03', 'F04'
for well in wells:
    print('Processing well' + well)
    stk_to_cv7k_png(input_path, output_path, prefix, well, channels, 0, z_steps, sites, project=True)
    stk_to_cv7k_png(input_path, output_path, prefix, well, channels, 1,z_steps, sites, project = False)

# Change naming of input files
well = 'C03'
print('Processing well' + well)
stk_to_cv7k_png(input_path, output_path, prefix, well, channels, 0, z_steps, sites, project=True)
stk_to_cv7k_png(input_path, output_path, prefix, well, channels, 1, z_steps, sites, project = False)


wells = ['C03', 'D03', 'D04', 'E03', 'E04']  #
output_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle2-DDX6_PNGs/'
input_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle2/'
prefix = 'R20181207-Stellaris4-DDX6'
for well in wells:
    print('Processing well' + well)
    stk_to_cv7k_png(input_path, output_path, prefix, well, channels, 0, z_steps, sites, project=True)
    stk_to_cv7k_png(input_path, output_path, prefix, well, channels, 2,z_steps, sites, project = False)
    stk_to_cv7k_png(input_path, output_path, prefix, well, channels, 3, z_steps, sites, project=True)


def stk_to_cv7k_png_change_sites(input_path, output_path, prefix, well, channels, curr_channel_number,z_steps, input_sites, project = True):
    channel_numbers = ['01', '02', '03', '04']

    for j, site in enumerate(input_sites):
        print(site)
        filename = os.path.join(input_path, prefix + '-' + well + '-3_' + channels[curr_channel_number] + '_s' + str(site) + '.stk')
        bf_reader = bf.ImageReader(filename, perform_init= True)
        # md = bf.get_omexml_metadata(filename)
        # print(xml_pretty.parseString(md.encode('utf-8')).toprettyxml())

        # Load all z dims, then project
        size = [z_steps,2048, 2048]
        if project == True:
            img = np.empty(size, np.uint16)

            output_filename = prefix + '_' + well + '_' + 'T001F' + str(j).zfill(3) + 'L01A01Z01C' + channel_numbers[
                curr_channel_number] + '.png'

            for i in range(z_steps):
                img[i] = bf_reader.read(z = i, t=0, rescale=False)
            projected_img = img.max(axis=0)


            cv2.imwrite(os.path.join(output_path,  output_filename), projected_img)

        if project == False:
            for i in range(z_steps):
                # img = np.empty(size[1:], np.uint16)
                output_filename = prefix + '_' + well + '_' + 'T001F' + str(j).zfill(3) + 'L01A01Z' + str(i+1).zfill(3) + \
                                  'C' + channel_numbers[curr_channel_number] + '.png'
                img = bf_reader.read(z=i, t=0, rescale=False)

                cv2.imwrite(os.path.join(output_path, output_filename), img)


input_sites = [9, 10, 11, 12, 13,
               16, 17, 18, 19, 20,
               23, 24, 25, 26, 27,
               30, 31, 32, 33, 34,
               37, 38, 39, 40, 41]
output_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle2-DDX6_PNGs/'
input_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle2/'
prefix = 'R20181207-Stellaris4-DDX6'
well = 'C04'
print('Processing Cycle 2, well ' + well)
stk_to_cv7k_png_change_sites(input_path, output_path, prefix, well, channels, 0, z_steps, input_sites, project=True)
stk_to_cv7k_png_change_sites(input_path, output_path, prefix, well, channels, 2, z_steps, input_sites, project=False)
stk_to_cv7k_png_change_sites(input_path, output_path, prefix, well, channels, 3, z_steps, input_sites, project=True)


# Create filler images (for C05, C06 for cycle 2)

def filler_to_cv7k_png(output_path, well, curr_channel_number,z_steps, sites, project = True):
    channel_numbers = ['01', '02', '03', '04']
    size = [2048, 2048]
    img = np.ones(size, np.uint16) * 110
    for site in sites:

        if project:
            output_filename = prefix + '_' + well + '_' + 'T001F' + str(site).zfill(3) + 'L01A01Z01C' + channel_numbers[
                curr_channel_number] + '.png'

            cv2.imwrite(os.path.join(output_path,  output_filename), img)

        if not project:
            for i in range(z_steps):
                output_filename = prefix + '_' + well + '_' + 'T001F' + str(site).zfill(3) + 'L01A01Z0' + str(i+1) + \
                                  'C' + channel_numbers[curr_channel_number] + '.png'

                cv2.imwrite(os.path.join(output_path, output_filename), img)

wells = ['C05', 'C06']  # 'C03', 'C05', 'C06',
output_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle2-DDX6_PNGs/'
input_path = '/Users/Joel/shares/dataShareJoel/jluethi/20181207-Stellaris-4/Cycle2/'
prefix = 'R20181207-Stellaris4-DDX6'
for well in wells:
    print('Processing well' + well)
    filler_to_cv7k_png(output_path, well, 0, z_steps, sites, project=True)
    filler_to_cv7k_png(output_path, well, 2,z_steps, sites, project = False)
    filler_to_cv7k_png(output_path, well, 3, z_steps, sites, project=True)


# plt.imshow(projected_img)
# plt.show()

jv.kill_vm()



