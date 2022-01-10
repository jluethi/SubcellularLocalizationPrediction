# Utility script to download all the illum_corr image files for 1 wavelength
import os
import json
from tmclient.api import TmClient
import shutil
import yaml
# import png
import sys
import requests
# import numpy as np
# import cv2

# Variables to be set before using the script
host="172.23.47.46"
port = 80
experimentName="20180601-SLP_Multiplexing"
username="joel"
password="123456"
output_path = '/data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/SLP_feature_values/'
mapobject_type = 'Cells'

# Create tmclient instance
client_general = TmClient(host, port, username, password, experimentName)

# Get plate name
plateDownload = client_general.get_plates()
plate_name = plateDownload[0]['name']

# Get list of wells
wells = client_general.get_wells(plate_name = plate_name)

index = int(sys.argv[1])
well_id = wells[index]

well = well_id.get('name')
print(well)
filename_metadata = os.path.join(output_path, 'Metadata_' + well + '.csv')
metadata = client_general.download_object_metadata(mapobject_type_name = mapobject_type, well_name = well)
metadata.to_csv(filename_metadata, index=False)
