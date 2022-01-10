import sys
import subprocess
import os

image_path = "/data/active/jluethi/20180730_bDNA-FISH_Pbodies/images"
project_path = "/data/active/jluethi/20180730_bDNA-FISH_Pbodies/Pbody_classifier.ilp"
file_ending = 'C04.png'

file_list_tmp = os.listdir(image_path)
file_list = []

for fyle in file_list_tmp:
    if fyle.endswith(file_ending):
        file_list.append(fyle)
    
batch_size = 30

index = int(sys.argv[1]) * batch_size

# Use readonly option to allow multiple nodes to access the project at once. See here for details:
# https://github.com/ilastik/ilastik/issues/1994
command = ['run_ilastik.sh', '--headless', '--project', project_path, '--readonly=1']

for i in range(batch_size):
    if index + i < len(file_list):
        current_image = os.path.join(image_path, file_list[index + i])
        command.append(current_image)

subprocess.call(command)