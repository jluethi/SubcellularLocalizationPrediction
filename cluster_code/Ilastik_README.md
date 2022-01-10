How to use Ilastik on the cluster

1) Prepare Ilastik pipeline correctly
2) Adapt run_Ilastik.py & arrayjob_Ilastik.sh scripts to your usecase
3) Submit to cluster

1)
The Ilastik classifier needs to be trained in the interface and the export options need to be specified in the "Prediction Export" part of the Ilastik interface. For upload to TissueMaps, one wants:
- Cutout Subregion, only export **1 channel from c**. Typically, one has 2 (background & object). Export only the object channel.
- Convert to Data Type: **unsigned 16-bit** (unless the other images are e.g. 8bit)
- Renormalize [min, max] from 0.00 1.00 to **0 65535**
- Format: png (unless one's input images for TissueMaps are still TIFFs)
- File: Adapt the path to where the cluster should save it (=> will only work on the cluster, not locally anymore). E.g.: /data/active/jluethi/ExperimentFolder/{nickname}_{result_type}.png

2)
- In run_Ilastik.py, **paths and file_ending** need to be adapted to the dataset (lines 5-7). 
- The **batch_size** can be change to a desired value (currently 30). Larger batch sizes means that one run_job computes more images => saves time in loading the pipeline, but means the later images wait until the earlier ones are processed.
- Line 4 in arrayjon_Ilastik.sh needs to be adapted:
	#SBATCH --array=0-51
	The X in 0-X needs to be set to (number_of_files)/batch_size
	
3)
Submit job to cluster by calling:
sbatch arrayjob_Ilastik.sh
(both arrayjob_Ilastik.sh and run_Ilastik.py are in the same folder)
