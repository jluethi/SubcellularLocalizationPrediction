#!/bin/bash

# Set up variables
EXP_NAME='20190927-Cardiomyocytes-StartDifferentiation'
plate='p1'
base_path='/data/active/jluethi/20190901-CardiomyocyteDifferentiationMultiplexing/'
path_part2='/image_links/start_subset/'

# instance & user name
inst='172.23.178.177'
user='jluethi'

# Read Password
echo -n Password: 
read -s password
echo

for cycle in 'Cycle1' 'Cycle2' 'Cycle4' 'Cycle5' 'Cycle6' 'Cycle7'
do
    img_path="$base_path$cycle$path_part2"
    echo "Registering images at $img_path as acquisition $cycle"
    tm_client -H $inst -u $user -p $password microscope-file -e $EXP_NAME register -p $plate -a $cycle $img_path
done    
