# Script to read in the IBM Tivoli Storage Manager output & list all unique archive descriptions
import os
import csv

# filepath = '/Users/Joel/shares/workShareJoel/jluethi_active.2018-12-05.lst'
#
# with open(filepath, 'r') as f:
#     content = f.readlines()
#
# print(content[14:50])
#
# with open('tmp_list.lst', 'wb') as f:
#     filewriter = csv.writer(f, delimiter = ' ')
#     filewriter.writerows([content[0:1000]])

# filepath = '/Users/Joel/Dropbox/Joel/PelkmansLab/Code/PyCharm/DeepLearning/tmp_list.lst'
filepath = '/Users/Joel/shares/workShareJoel/jluethi_active.2018-12-05.lst'

with open(filepath, 'r') as f:
    content = f.readlines()

filename_content = content[14:]

unique_folders = set()

for file_description in filename_content:
    current_folder_name = file_description.split()[-1]
    unique_folders.add(current_folder_name)

print('Unique elements backed up:' + str(len(unique_folders)))
for element in unique_folders:
    print(element)

with open('backed_up_folders.txt', 'wb') as f:
    folders_output = list(unique_folders)
    folders_output.sort()
    for element in folders_output:
        f.write(element + '\n')



