# Utility script to download all the segmentations from an experiment

import os
import json
from tmclient.api import TmClient
import shutil
import yaml
import png
import sys
import requests
import numpy as np
import cv2

# Variables to be set by the user before using the script
host="172.23.47.46"
experimentName="20180730_bDNA-FISH_Pbodies"
username="joel"
password="123456"
mapobject="Cells"
output_path = '/data/active/jluethi/20180730_bDNA-FISH_Pbodies/segmentations_Cells/' # Path where the images will be saved
will_align = False # Recommended to set True if segmentations for a multiplexing experiment are downloaded
channelName = 'A01_C01' # Name of any channel in the first cycle

# Parameters that the user normally doesn't need to change
port = 80
cycle_index = 0  # Cycle index of first channel name (used as backup if there is no segmentation image for a site)

# Create tmclient instance
client_general = TmClient(host, port, username, password, experimentName)
# print json.dumps(mapobject_download,sort_keys=True, indent = 4, separators=(',', ': '))

# Get plate name
plateDownload = client_general.get_plates()
plate_name = plateDownload[0]['name']

# Get list of wells
wells = client_general.get_wells(plate_name = plate_name)

index = int(sys.argv[1])
well_id = wells[index]
# Initiate a new client instance per well, so that the token doesn't expire
client = TmClient(host, port, username, password, experimentName)
well = well_id.get('name')
print(well)
sites = client.get_sites(plate_name = plate_name, well_name = well)

# Loop through all sites, download segmentation
for site in sites:
    x = site.get('x')
    y = site.get('y')
    filename = os.path.join(output_path, experimentName +'Segmentation_' +
        mapobject +'_plate_' + plate_name + '_well_' + well +
        '_x' + str(x) + 'y' + str(y) + '.png')

    # This download fails with an error message if there is no mapobject in the specified site
    try:
        segmentation = client.download_segmentation_image(mapobject_type_name = mapobject,
            plate_name = plate_name, well_name = well, well_pos_y = y, well_pos_x = x,
            tpoint=0, zplane=0, align = will_align)

        ImageHeight = segmentation.shape[0]
        ImageWidth = segmentation.shape[1]

    except requests.exceptions.HTTPError:
        print('No objects of type ' + mapobject + ' in ' + well + '_x' +
            str(x) + '_y' + str(y) + '. Downloading an empty segmentation image instead.')
        # Because there is no actual object, one needs to figure out the dimensions of the segmentation image
        # channel_names = client.get_channels()
        # channelName = channel_names[0].get('name')
        response = client._download_channel_image(channel_name = channelName,
                        plate_name = plate_name, well_name = well,
                        well_pos_y = y, well_pos_x = x, cycle_index = cycle_index,
                        tpoint=0, zplane=0, correct = False, align = will_align)

        data = np.frombuffer(response.content, np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
        ImageHeight = img.shape[0]
        ImageWidth = img.shape[1]

        segmentation = np.zeros([ImageHeight, ImageWidth])


    f = open(filename, 'wb')
    w = png.Writer(width = ImageWidth, height = ImageHeight, bitdepth = 16, greyscale=True)
    w.write(f, segmentation)
    f.close()
