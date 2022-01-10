#!/bin/bash

# Set up variables
# cycle='Cycle1'
# img_base_name='20190902-JL-CardiomyociteDifferentiationMultiplexing-'
# cycle='Cycle2'
# img_base_name='20190906-JL-CardiomyociteDifferentiationMultiplexing-'
# cycle='Cycle3'
# img_base_name='20190907-JL-CardiomyociteDifferentiationMultiplexing-'
# cycle='Cycle4'
# img_base_name='20190908-JL-CardiomyociteDifferentiationMultiplexing-'
# cycle='Cycle5'
# img_base_name='20190909-JL-CardiomyociteDifferentiationMultiplexing-'
# cycle='Cycle6'
# img_base_name='20190910-JL-CardiomyociteDifferentiationMultiplexing-'
# cycle='Cycle7'
# img_base_name='20190911-JL-CardiomyociteDifferentiationMultiplexing-'
cycle='Cycle11'
img_base_name='20190917-CardiomyociteDifferentiationMultiplexing-'

# General variables
base_path='/data/active/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/'
path_part2='/image_links/'

target_base_path='/data/active/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/20190923_SitesOfInterest/'
cycle_name=$cycle

mkdir $target_base_path$cycle

# Well D02
# Get the images for undifferentiated cells
well='D02'
img_name=$img_base_name$cycle_name'_'$well'_'
site='079'
ln $base_path$cycle$path_part2'undifferentiated/'$img_name'T0001F'$site*'C01.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'undifferentiated/'$img_name'T0001F'$site*'C02.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'undifferentiated/'$img_name'T0001F'$site*'C03.png' $target_base_path$cycle

# Create filler images in Z (22 - 35)
for z_level in {22..35}
do
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C01.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C02.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A02Z'$z_level'C03.png'
done

# # Rename to site 1
cd $target_base_path$cycle
rename 's/F'$site'/F001/' $img_name*



# Well F02
well='F02'
img_name=$img_base_name$cycle_name'_'$well'_'
site='025'
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C01.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C02.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C03.png' $target_base_path$cycle

# Create filler images in Z (30 - 35)
for z_level in {30..35}
do
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C01.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C02.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A02Z'$z_level'C03.png'
done

# # Rename to site 1
cd $target_base_path$cycle
rename 's/F'$site'/F001/' $img_name*
rename 's/T0002/T0001/' $img_name*


# Well D04
well='D04'
img_name=$img_base_name$cycle_name'_'$well'_'
site='059'
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C01.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C02.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C03.png' $target_base_path$cycle

# Create filler images in Z (30 - 35)
for z_level in {30..35}
do
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C01.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C02.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A02Z'$z_level'C03.png'
done

# # Rename to site 1
cd $target_base_path$cycle
rename 's/F'$site'/F001/' $img_name*
rename 's/T0002/T0001/' $img_name*


# Well F04
well='F04'
img_name=$img_base_name$cycle_name'_'$well'_'
site='022'
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C01.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C02.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'start_differentiation/'$img_name'T0002F'$site*'C03.png' $target_base_path$cycle

# Create filler images in Z (30 - 35)
for z_level in {30..35}
do
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C01.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A01Z'$z_level'C02.png'
    ln $target_base_path'BlackZFiller.png' $target_base_path$cycle'/'$img_name'T0001F'$site'L01A02Z'$z_level'C03.png'
done

# # Rename to site 1
cd $target_base_path$cycle
rename 's/F'$site'/F001/' $img_name*
rename 's/T0002/T0001/' $img_name*



# Well D06
well='D06'
img_name=$img_base_name$cycle_name'_'$well'_'
site='052'
ln $base_path$cycle$path_part2'differentiated/'$img_name'T0003F'$site*'C01.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'differentiated/'$img_name'T0003F'$site*'C02.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'differentiated/'$img_name'T0003F'$site*'C03.png' $target_base_path$cycle

# # Rename to site 1
cd $target_base_path$cycle
rename 's/F'$site'/F001/' $img_name*
rename 's/T0003/T0001/' $img_name*


# Well F06
well='F06'
img_name=$img_base_name$cycle_name'_'$well'_'
site='023'
ln $base_path$cycle$path_part2'differentiated/'$img_name'T0003F'$site*'C01.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'differentiated/'$img_name'T0003F'$site*'C02.png' $target_base_path$cycle
ln $base_path$cycle$path_part2'differentiated/'$img_name'T0003F'$site*'C03.png' $target_base_path$cycle

# # Rename to site 1
cd $target_base_path$cycle
rename 's/F'$site'/F001/' $img_name*
rename 's/T0003/T0001/' $img_name*


# For cycle 11: Also copy C04 and rename to C02. Don't copy C02