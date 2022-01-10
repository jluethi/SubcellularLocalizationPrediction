# Utility script to download all the illum_corr image files for 1 wavelength
# import os
# import json
from tmclient.api import TmClient
# import shutil
# import yaml
# import png
import sys
# import requests
# import numpy as np
# import cv2

# Variables to be set before using the script
#host="cluster.pelkmanslab.org"
host="172.23.178.177"
port = 80
experimentName="20190917-Cardiomyocyte-Multiplexing_Differentiated"
username="jluethi"
password="Cora-Cardiff-emergent-glitzy"
output_path = '/data/homes/jluethi/20190923_CardiomyocytePoster/overview_singleChannel_cycle2'
will_align = False
illum_corr = False
# cycle_indices = [8,8,9,9,10,10,10,10,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7]
# channel_names = ['10_Paxillin', '10_Pericentrin','11_EEA1','11_Sara','13_DCP1a',
#             '13_DDX6','13_Pbody_Segm', '13_Succs', '1_Lamp1', '1_PCNA',
#             '2_Calreticulin', '2_DAPI', '3_APPL', '3_GM130', '4_HSP60',
#             '4_LC3B', '5_pS6', '5_Yap', '7_Acetyl_Tubulin', '7_Actin',
#             '8_Caveolin', '8_Pol2', '9_ABCD3']
#cycle_indices = ['1', '1', '1']
# cycle_indices = ['7', '0', '0', '0', '1', '1', '3', '4', '4', '5', '6']
# channel_names = ['11_Tubulin', '1_DAPI', '1_nanog', '1_Troponin', '2_bCatenin', '2_NaKATPase', '4_LaminB1', '5_Glut1', '5_HSP60', '6_GM130', '7_EEA1']
#cycle_indices = ['7', '0', '0', '0', '1', '1', '3', '4', '4', '5', '6']
#channel_names = ['11_Tubulin', '1_DAPI', '1_nanog', '1_Troponin', '2_bCatenin', '2_NaKATPase', '4_LaminB1', '5_Glut1', '5_HSP60', '6_GM130', '7_EEA1']
cycle_indices = ['2', '2']
channel_names = ['2_A01_C02', '2_A01_C01']

# Create tmclient instance
client_general = TmClient(host, port, username, password, experimentName)
# print json.dumps(mapobject_download,sort_keys=True, indent = 4, separators=(',', ': '))

# Get plate name
plateDownload = client_general.get_plates()
plate_name = plateDownload[0]['name']

# Get list of wells
#wells = client_general.get_wells(plate_name = plate_name)
wells = ['F06']
# wells = ['D02', 'F02', 'D04', 'F04', 'D06', 'F06']
#wells = ['D06', 'F06', 'D08']

index = int(sys.argv[1])
#well_id = wells[index]
well = wells[index]

#well = well_id.get('name')
print(well)
sites = client_general.get_sites(plate_name = plate_name, well_name = well)

# Loop through all channels of interest
for i, channelName in enumerate(channel_names):
    cycle_index = cycle_indices[i]

    # Initiate a new client instance per well, so that the token doesn't expire
    client = TmClient(host, port, username, password, experimentName)

    # Loop through all sites, download segmentation
    for site in sites:
        x = site.get('x')
        y = site.get('y')

        client.download_channel_image_file(channel_name = channelName, plate_name = plate_name, well_name = well,
                                           well_pos_y = y, well_pos_x = x, cycle_index = cycle_index, tpoint=0, zplane=0,
                                           correct = illum_corr, align = will_align, directory = output_path)
