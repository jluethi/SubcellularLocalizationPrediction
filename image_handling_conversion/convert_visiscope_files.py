# Convert visiscope stacks of 20190325_gfp experiment to pngs when files don't contain well name
import bioformats as bf
import javabridge as jv
import numpy as np
import cv2
import os

print('Starting')

jv.start_vm(class_path=bf.JARS, max_heap_size='4G')

def stk_to_cv7k_png(input_path, output_path, prefix, channels, well, site, z_steps, project = False):
    channel_numbers = ['01', '02', '03', '04']
    for curr_channel_number in range(len(channels)):
        filename = os.path.join(input_path, prefix + '_'+ channels[curr_channel_number] + '_s' + str(site) + '.stk')
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
                output_filename = prefix + '_' + well + '_' + 'T001F' + str(site).zfill(3) + 'L01A01Z' + str(i+1).zfill(2) + \
                                  'C' + channel_numbers[curr_channel_number] + '.png'
                img = bf_reader.read(z=i, t=0, rescale=False)

                cv2.imwrite(os.path.join(output_path, output_filename), img)


# prefix = '20190325-JL-WTCTubulin-gfp-ab-stain1'
# channels = ['w1sdcDAPIxmRFPm', 'w2sdcGFP-Cam1', 'w3sdcRFP590-20', 'w4sdcCy5']
# z_steps = 10
# output_path = '/Users/Joel/shares/dataShareJoel/jluethi/20190325-WTCTubulin_tubulinGFPAbStain/images/'
# input_path = '/Users/Joel/shares/dataShareJoel/jluethi/20190325-WTCTubulin_tubulinGFPAbStain/'
# # wells = [[list(range(1,37)), 'B02'], [list(range(37,73)), 'B03'], [list(range(73,108)), 'B04']]
# wells = [[[108], 'B04']]
#
# for curr_well in wells:
#     well = curr_well[1]
#     for site in curr_well[0]:
#         print('Processing site ' + str(site))
#         stk_to_cv7k_png(input_path, output_path, prefix, channels, well, site, z_steps, project = False)
#
# print('Finished')


def stk_to_cv7k_png(input_path, output_path, prefix, channels, well, site, z_steps, project = False):
    channel_numbers = ['01', '02', '03', '04']
    for curr_channel_number in range(len(channels)):
        filename = os.path.join(input_path, prefix + '_'+ channels[curr_channel_number] + '_s' + str(site) + '.stk')
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
            i = 9
            output_filename = prefix + '_' + well + '_' + 'T001F' + str(site).zfill(3) + 'L01A01Z' + str(i+1).zfill(2) + \
                              'C' + channel_numbers[curr_channel_number] + '.png'
            img = bf_reader.read(z=i, t=0, rescale=False)

            cv2.imwrite(os.path.join(output_path, output_filename), img)


prefix = '20190325-JL-WTCTubulin-gfp-ab-stain1'
channels = ['w1sdcDAPIxmRFPm', 'w2sdcGFP-Cam1', 'w3sdcRFP590-20', 'w4sdcCy5']
z_steps = 10
output_path = '/Users/Joel/shares/dataShareJoel/jluethi/20190325-WTCTubulin_tubulinGFPAbStain/images/'
input_path = '/Users/Joel/shares/dataShareJoel/jluethi/20190325-WTCTubulin_tubulinGFPAbStain/'
wells = [[list(range(1,37)), 'B02'], [list(range(37,73)), 'B03'], [list(range(73,109)), 'B04']]

for curr_well in wells:
    well = curr_well[1]
    for site in curr_well[0]:
        print('Processing site ' + str(site))
        stk_to_cv7k_png(input_path, output_path, prefix, channels, well, site, z_steps, project = False)

print('Finished')