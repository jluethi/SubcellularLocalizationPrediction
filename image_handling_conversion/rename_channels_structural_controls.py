import os
import shutil


base_base_path = '/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/'
# folder_names = ['Cycle1_PNG/', 'Cycle2_PNG/', 'Cycle3_PNG/', 'Cycle4_PNG/','Cycle5_PNG/', 'Cycle6_PNG/', 'Cycle7_PNG/',
#                 'Cycle8_PNG/','Cycle9_PNG/', 'Cycle10_PNG/', 'Cycle11_PNG/', 'Cycle13_PNG/']

folder_names = ['Cycle13_PNG/']

for folder_name in folder_names:
    print(folder_name)
    base_path = os.path.join(base_base_path, folder_name)
    source_folder = 'StructuralControls'
    target_folder = 'MainExperiment'
    source_path = os.path.join(base_path, source_folder)
    target_path = os.path.join(base_path, target_folder)
    # target_path = os.path.join('/Users/Joel/Desktop/', target_folder)
    file_list = os.listdir(source_path)

    # Go through all files, if the filename fulfills a condition, move a renamed copy
    # for file_name in file_list:
    #     if file_name.endswith('C05.png'):
    #         source_filename = os.path.join(source_path, file_name)
    #         destination_filename_new = os.path.join(target_path, file_name[:-21] + '3' + file_name[-20:-14] + '1' + file_name[-13:-7] + 'C03.png')
    #         shutil.copyfile(source_filename, destination_filename_new)
    #
    # for file_name in file_list:
    #     if file_name.endswith('C04.png'):
    #         source_filename = os.path.join(source_path, file_name)
    #         destination_filename_new = os.path.join(target_path,
    #                                                 file_name[:-21] + '3' + file_name[-20:-14] + '1' + file_name[
    #                                                                                                    -13:-7] + 'C02.png')
    #         shutil.copyfile(source_filename, destination_filename_new)
    #
    #
    # for file_name in file_list:
    #     if file_name.endswith('C01.png'):
    #         source_filename = os.path.join(source_path, file_name)
    #         destination_filename_new = os.path.join(target_path, file_name[:-21] + '3' + file_name[-20:-14] + '1' + file_name[-13:])
    #         shutil.copyfile(source_filename, destination_filename_new)

    for file_name in file_list:
        if file_name.endswith('C06.png'):
            source_filename = os.path.join(source_path, file_name)
            destination_filename_new = os.path.join(target_path, file_name[:-21] + '3' + file_name[-20:-14] + '1' + file_name[-13:])
            shutil.copyfile(source_filename, destination_filename_new)