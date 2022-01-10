# Utility script to download all the illumination corrected images for a given channel

import os
import json
from tmclient.api import TmClient
import shutil
import yaml
import png

# Variables to be set before using the script
host="172.23.47.46"
port = 80
experimentName="20180324_ShrinkageTest2"
username="joel"
password="TBD"
output_path = '/home/ubuntu/20180324_ShrinkageTest2_images/'

# Get channel name
channelName = raw_input("Enter Channel Name: ")

# Create tmclient instance
client_general = TmClient(host, port, username, password, experimentName)
# print json.dumps(mapobject_download,sort_keys=True, indent = 4, separators=(',', ': '))

# Get plate name
plateDownload = client_general.get_plates()
plate_name = plateDownload[0]['name']

# Get list of wells
wells = client_general.get_wells(plate_name = plate_name)

# Get list of sites per well
for well_id in wells:
    # Initiate a new client instance per well, so that the token doesn't expire
    client = TmClient(host, port, username, password, experimentName)
    well = well_id.get('name')
    print well
    sites = client.get_sites(plate_name = plate_name, well_name = well)

    # Loop through all sites, download segmentation
    for site in sites:
        x = site.get('x')
        y = site.get('y')
        # filename = output_path + experimentName +'_IllumCorrImage_' +'_plate_' + plate_name + '_well_' + well + '_x' + str(x) + 'y' + str(y) + '.png'

        client.download_channel_image_file(channel_name = channelName, plate_name = plate_name, well_name = well,
                                           well_pos_y = y, well_pos_x = x, cycle_index = '0', tpoint=0, zplane=0,
                                           correct = True, align = True, directory = output_path)
