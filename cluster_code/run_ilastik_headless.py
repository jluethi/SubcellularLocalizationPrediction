# Script to run Ilastik in headless mode on the cluster
# Load the Ilastik module in the bash script by calling: module load Ilastik

import subprocess

subprocess.call(['run_ilastik.sh', '--headless'])

















