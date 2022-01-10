#! /bin/sh
# Write output to slurm-$JOBID_$TASKID.txt
#SBATCH -o slurm-%j_%a.txt
#SBATCH -e slurm_error-%j_%a.txt
#SBATCH --mem-per-cpu=3000m
#SBATCH -c 8

#exec python convert_tiff_to_png.py /data/active/jluethi/20180116-SecAbTest2-Plastic/AssayPlate_Greiner_#655090 /data/active/jluethi/20180116-SecAbTest2-Plastic/images
exec python convert_tiff_to_png.py /data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/Cycle13 /data/active/jluethi/20180503-SubcellularLocalizationMultiplexing/Cycle13_PNG
