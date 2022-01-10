#!/bin/bash

# Set up variables
cycle='Cycle11'
cycle_name='Cycle11'
#img_base_name='20190912-JL-CardiomyociteDifferentiationMultiplexing-'
img_base_name='20190917-CardiomyociteDifferentiationMultiplexing-'

# General variables
base_path='/data/active/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/'
path_part2='/image_links/'

# Create the directories
mkdir $base_path$cycle'/image_links'
mkdir $base_path$cycle$path_part2'undifferentiated'
mkdir $base_path$cycle$path_part2'start_differentiation'
mkdir $base_path$cycle$path_part2'differentiated'

# Link files for undifferentiated
ln $base_path$cycle'/images/'$img_base_name$cycle_name'_C02'* $base_path$cycle$path_part2'undifferentiated'
ln $base_path$cycle'/images/'$img_base_name$cycle_name'_D02'* $base_path$cycle$path_part2'undifferentiated'
ln $base_path$cycle'/images/'$img_base_name$cycle_name'_F10'* $base_path$cycle$path_part2'undifferentiated'
ln $base_path$cycle'/images/'$img_base_name$cycle_name'_G10'* $base_path$cycle$path_part2'undifferentiated'

# Rename the files for wells F10 & G10 to timepoint 1 (for TissueMaps reasons)
cd $base_path$cycle$path_part2'undifferentiated'
rename 's/T0004/T0001/' *'C01.png'
rename 's/T0004/T0001/' *'C02.png'
rename 's/T0004/T0001/' *'C03.png'

# Link files for start_differentiation
for site in 00 01 02 03 04 05 06 07 08 09 10
do
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_F02_T0002F'$site* $base_path$cycle$path_part2'start_differentiation'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_G02_T0002F'$site* $base_path$cycle$path_part2'start_differentiation'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_C04_T0002F'$site* $base_path$cycle$path_part2'start_differentiation'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_D04_T0002F'$site* $base_path$cycle$path_part2'start_differentiation'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_F04_T0002F'$site* $base_path$cycle$path_part2'start_differentiation'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_G04_T0002F'$site* $base_path$cycle$path_part2'start_differentiation'
done


# Link files for differentiated
for site in 00 01 02 03 04 05 06 07 08 09 10
do
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_C06_T0003F'$site* $base_path$cycle$path_part2'differentiated'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_D06_T0003F'$site* $base_path$cycle$path_part2'differentiated'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_F06_T0003F'$site* $base_path$cycle$path_part2'differentiated'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_G06_T0003F'$site* $base_path$cycle$path_part2'differentiated'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_C08_T0003F'$site* $base_path$cycle$path_part2'differentiated'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_D08_T0003F'$site* $base_path$cycle$path_part2'differentiated'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_F08_T0003F'$site* $base_path$cycle$path_part2'differentiated'
    ln $base_path$cycle'/images/'$img_base_name$cycle_name'_G08_T0003F'$site* $base_path$cycle$path_part2'differentiated'
done
