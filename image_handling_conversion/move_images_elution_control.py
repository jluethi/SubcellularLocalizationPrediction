import os
import shutil
import re

base_path = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/'
# base_path = '/Users/Joel/Desktop/'
list_of_dirs = ['Cycle1_PNG', 'Cycle2_PNG', 'Cycle3_PNG', 'Cycle4_PNG', 'Cycle5_PNG', 'Cycle7_PNG', 'Cycle8_PNG', 'Cycle9_PNG', 'Cycle10_PNG', 'Cycle11_PNG', 'Cycle13_PNG']
target_stainings = os.path.join(base_path, 'AntibodyElutions/1_stainings')
target_elutions = os.path.join(base_path, 'AntibodyElutions/2_elution')

move_to_stainings = ['E12', 'E13', 'E14', 'E15', 'E16', 'F13', 'F14', 'F15', 'F16', 'E12', 'E14']
move_to_elutions = ['', 'E12', 'E13', 'E14', 'E15', 'F12', 'F13', 'F14', 'F15', 'F16', 'E12']

rename_staining = ['A01', 'A02', 'A03', 'A04', 'A05', 'A07', 'A08', 'A09', 'A10', 'A11', 'A13']
rename_elution = ['', 'A01', 'A02', 'A03', 'A04', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11']

# Non used acquisitions:
# Cycle 3 contains reimaged versions of well E12 elution, much lower signal for 488 images
# Cycle 10: Imaged well E12 again before reusing it in cycle 11. Noise in 488, 561 is clean

# Go through all acquisitions and divide images into staining & elution folder + rename wells
for index, input_folder in enumerate(list_of_dirs):
    source_path = os.path.join(os.path.join(base_path, input_folder),'AntibodyElutionTests')
    file_list = os.listdir(source_path)
    staining_path = os.path.join(base_path, target_stainings)

    for file_name in file_list:
        regexp_staining = re.compile('_' + move_to_stainings[index] + '_')
        regexp_elutions = re.compile('_' + move_to_elutions[index] + '_')
        source_filename = os.path.join(source_path, file_name)

        if regexp_staining.search(file_name):
            if not file_name.endswith('C06.png'):
                destination_filename_new = os.path.join(target_stainings, file_name[:-29] + rename_staining[index] + file_name[-26:])
                shutil.copyfile(source_filename, destination_filename_new)

        if regexp_elutions.search(file_name):
            if not file_name.endswith('C06.png'):
                destination_filename_new = os.path.join(target_elutions, file_name[:-29] + rename_elution[index] + file_name[-26:])
                shutil.copyfile(source_filename, destination_filename_new)


# Distribute Succs images
move_to_succs = ['E12', 'E13', 'E14', 'E15', 'E16', 'F12', 'F13', 'F14', 'F15', 'F16', 'E12', 'E14']
rename_succs = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06' ,'A07', 'A08', 'A09', 'A10', 'A11', 'A13']
target_succs = os.path.join(base_path, 'AntibodyElutions/3_succs')

source_path = os.path.join(os.path.join(base_path, 'Cycle13_PNG/'),'AntibodyElutionTests')
file_list = os.listdir(source_path)
staining_path = os.path.join(base_path, target_stainings)

for well_index in range(len(move_to_succs)):
    regexp_succs = re.compile('_' + move_to_succs[well_index] + '_')

    for file_name in file_list:
        if regexp_succs.search(file_name):
            # if not (file_name.endswith('C01.png') or file_name.endswith('C06.png')):
            source_filename = os.path.join(source_path, file_name)
            destination_filename_new = os.path.join(target_succs, file_name[:-29] + rename_succs[well_index] + file_name[-26:])
            shutil.copyfile(source_filename, destination_filename_new)



