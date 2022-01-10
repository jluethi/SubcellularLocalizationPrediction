# Script to create filler images for tissuemaps for missing images
import numpy as np
import png
import os

target_folder = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/Cycle1_PNG/MainExperiment/'
nb_sites = 36
wells = ['E11', 'F11']
filename_base = 'AssayPlate_Greiner_781091_'
channel_name = 'C03'
action_number = 'A03'
background_level = 115
empty_image = np.ones(shape=[2160, 2560]) * background_level


for well in wells:
    for site in range(1,nb_sites+1):
        filename = filename_base + well + '_T0003F' + str(site).zfill(3) + 'L01' + action_number + 'Z01' + channel_name + '.png'
        filepath = os.path.join(target_folder, filename)
        with open(filepath, 'wb') as f:
            writer = png.Writer(width=empty_image.shape[1], height=empty_image.shape[0], bitdepth=16, greyscale=True)
            writer.write(f, empty_image)



