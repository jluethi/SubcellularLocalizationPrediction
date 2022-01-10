# Utility script to download all the illumination corrected images for a given channel

from tmclient.api import TmClient
import sys

# Variables to be set before using the script
host="172.23.47.46"
port = 80
experimentName="20180421-AntibodyPanelTest"
username="joel"
password="123456"
output_path = '/data/active/jluethi/20180418-AntibodyPanelTest/IllumCorrImages/'

# Get channel name
index = int(sys.argv[1])
channelNames = ['Cycle1_488', 'Cycle1_568', 'Cycle1_DAPI','ElutionRestain_488', 'ElutionRestain_568', 'ElutionRestain_DAPI','Cycle10_488', 'Cycle10_568', 'Cycle10_DAPI', 'Cycle10_Succs']
channelName = channelNames[index]

cycle_indices = ['0', '0', '0', '1', '1', '1', '2', '2', '2', '2']

# Create tmclient instance
client_general = TmClient(host, port, username, password, experimentName)
# print json.dumps(mapobject_download,sort_keys=True, indent = 4, separators=(',', ': '))

# Get plate name
plateDownload = client_general.get_plates()
plate_name = plateDownload[0]['name']

# Get list of all wells
wells = client_general.get_wells(plate_name = plate_name)

# Get list of sites per well
# well_list = []
# for row in ['C', 'D']:
#     for col in range(2,18):
#         well_name = row + '%02d' % col
#         well_list.append(well_name)
# for well in wells:

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
