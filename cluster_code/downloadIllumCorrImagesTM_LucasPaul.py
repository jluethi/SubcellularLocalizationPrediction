# Utility script to download all the illumination corrected images for a given channel

from tmclient.api import TmClient
import sys

### Variables to be set before using the script
host="HOST_IP"
port = 80
experimentName="EXPERIMENT_NAME"
username="USERNAME"
password="PASSWORD"
output_path = 'PATH_TO_OUTPUT_FOLDER'

# Fill the lists with the channel names and their corresponding cycle indices
channelNames = ['Cycle1_488', 'Cycle1_568', 'Cycle1_DAPI','ElutionRestain_488', 'ElutionRestain_568', 'ElutionRestain_DAPI','Cycle10_488', 'Cycle10_568', 'Cycle10_DAPI', 'Cycle10_Succs']
cycle_indices = ['0', '0', '0', '1', '1', '1', '2', '2', '2', '2']

### Script to download all images
# Create tmclient instance
client_general = TmClient(host, port, username, password, experimentName)

# Get plate name
plateDownload = client_general.get_plates()
plate_name = plateDownload[0]['name']

# Get list of all wells
wells = client_general.get_wells(plate_name = plate_name)

for index, channelName in enumerate(channelNames):
    for well_id in wells:
        well = well_id.get('name')

        # Initiate a new client instance per well, so that the token doesn't expire
        client = TmClient(host, port, username, password, experimentName)
        print well
        sites = client.get_sites(plate_name = plate_name, well_name = well)

        # Loop through all sites, download illumCorr image
        for site in sites:
            x = site.get('x')
            y = site.get('y')
            client.download_channel_image_file(channel_name = channelName, plate_name = plate_name, well_name = well,
                                               well_pos_y = y, well_pos_x = x, cycle_index = cycle_indices[index], tpoint=0, zplane=0,
                                               correct = True, align = True, directory = output_path)
