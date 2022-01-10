#! /bin/sh

# Submit a job array with index values between 0 and 5 (inclusive)
#SBATCH --array=0-51

# Write output to slurm-$JOBID_$TASKID.txt
#SBATCH -o slurm-%j_%a.txt
#SBATCH -e slurm_error-%j_%a.txt
### use (max) 2000 MB of memory per CPU
#SBATCH --mem-per-cpu=6000m

n="$SLURM_ARRAY_TASK_ID"

# load the ‘module‘ command if using an .sh script. In bash scripts, that's not necessary on the cluster
#. "/etc/profile.d/lmod.sh"
. "/etc/profile.d/lmod.sh"
module load Ilastik

exec python run_Ilastik.py $n
