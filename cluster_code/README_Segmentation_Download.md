# Quick Tutorial TissueMaps Segmentation Mask Download

Using the following 2 scripts, you can parallelize the download of segmentation images over the cluster:
1. arrayjob_segmentationDownload.sh
2. downloadAlignedSegmentationsTM.py

Setup
------
Create a virtual environment that contains all the dependencies and install the dependencies there:
```
mkvirtualenv segmentation_download
pip install pypng
pip install opencv-python
git clone https://github.com/TissueMAPS/TissueMAPS
cd TissueMAPS/tmclient
pip install .
cd ../..
```

Parameters to adapt in bash script
------
Change the last number in `#SBATCH --array=0-13` to your number of wells - 1 (e.g.: 24 wells => `#SBATCH --array=0-23`)
Change the name and location of the virtual environment to the one you just created, e.g. `venv="$HOME/.virtualenvs/segmentation_download"`


Parameters to adapt in python script
------
Change all the variable in the section **Variables to be set by the user before using the script** for your experiment.
You need to specify a channel name in your first cycle so that the script can deal with sites that have no segmentations.
