# Stitch well overviews based on downloaded files from TissueMaps
import numpy as np
import imageio
from pathlib import Path

target_directory = Path('/Users/Joel/shares/workShareJoel/20190923_CardiomyocytePoster/overview_singleChannel_cycle2/')

well_name = 'F06'
channels = ['2_A01_C01', '2_A01_C02']  #'A02_C03'

base_path = Path('/Users/Joel/shares/workShareJoel/20190923_CardiomyocytePoster/overview_singleChannel_cycle2/')
base_filename = '20190917-Cardiomyocyte-Multiplexing_Differentiated_p1_' + well_name

for channel in channels:
    # Target size: 10 images vertical, 9 images horizontal  => 21'600 x 23'040
    target_img = np.zeros((21600, 23040), np.uint16)
    for x in range(9):
        print(x)
        for y in range(10):
            img_path = base_path / (base_filename + '_y' + str(y).zfill(3) + '_x' + str(x).zfill(3) + '_z000_t000_' +
                                    channel + '.png')

            img = imageio.imread(img_path)
            target_img[y*2160:(y+1)*2160, x*2560:(x+1)*2560] = img

    output_path = target_directory / (base_filename + '_' + channel + '_Cycle2_stitched.png')
    imageio.imsave(output_path, target_img)


