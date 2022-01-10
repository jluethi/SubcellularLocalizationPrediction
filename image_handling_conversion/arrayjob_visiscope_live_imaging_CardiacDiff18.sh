#! /bin/sh

# Submit a job array with index values between 0 and 5 (inclusive)
#SBATCH --array=0-41%15

# Write output to slurm-$JOBID_$TASKID.txt
#SBATCH -o slurm-%j_%a.txt
#SBATCH -e slurm_error-%j_%a.txt
### use (max) 2000 MB of memory per CPU
#SBATCH --cpus-per-task=4
#SBATCH --mem=30000m

n="$SLURM_ARRAY_TASK_ID"


# activate virtualenv; `.` is an alias for `source` that also works in
# non-bash shells
venv="$HOME/.virtualenvs/visiscope"
if [ -r "$venv/bin/activate" ]; then
 . "$venv/bin/activate"
else
 echo 1>&2 "Cannot activate virtualenv '$venv'"
fi

# for debugging purposes, it's a good idea to print out the venv name
# and the actual python interpreter used
echo 1>&2 "Running in virtualenv '$venv', using python interpreter $(command -v python) ..."


exec python visiscope_live_imaging_CardiacDiff18.py $n
