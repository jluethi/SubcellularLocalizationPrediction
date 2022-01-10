from keras.models import load_model
import numpy as np
# import matplotlib.pyplot as plt
import cv2
import os
import glob
import re
from custom_loss_functions import subcellular_loss
from minibatch_generator import generate_testing_batch_from_path
from keras import backend as K
import tensorflow as tf
import csv
import datetime

# sess = tf.Session()
# K.set_session(sess)

# Load data
testing_path = '/home/joel/DeepLearning/20180502_SLP_Experiment/singleCellImages_dividedDatasets/test'

# Parameters
channel_names = ['2_DAPI', '10_Paxillin', '10_Pericentrin', '11_EEA1', '11_Sara', '13_DCP1a',
                 '13_DDX6', '13_Pbody_Segm', '13_Succs', '1_Lamp1', '1_PCNA',
                 '2_Calreticulin', '3_APPL', '3_GM130', '4_HSP60',
                 '4_LC3B', '5_pS6', '5_Yap', '7_Acetyl_Tubulin', '7_Actin',
                 '8_Caveolin', '8_Pol2', '9_ABCD3', 'segmentation']

list_input_output_combos = [[[0], [3, 23]],
                            [[0, 13], [3, 23]],
                            [[0, 9], [3, 23]],
                            [[0, 11], [3, 23]],
                            [[0, 14], [3, 23]],
                            [[0, 20], [3, 23]],
                            [[0, 21], [3, 23]],
                            [[0, 9, 11, 13, 14, 20, 21], [3, 23]],
                            [[0], [9, 23]],
                            [[0, 13], [9, 23]],
                            [[0, 3], [9, 23]],
                            [[0, 11], [9, 23]],
                            [[0, 14], [9, 23]],
                            [[0, 20], [9, 23]],
                            [[0, 21], [9, 23]],
                            [[0, 3, 11, 13, 14, 20, 21], [9, 23]],
                            [[0], [20, 23]],
                            [[0, 13], [20, 23]],
                            [[0, 3], [20, 23]],
                            [[0, 11], [20, 23]],
                            [[0, 14], [20, 23]],
                            [[0, 9], [20, 23]],
                            [[0, 21], [20, 23]],
                            [[0, 3, 9, 11, 13, 14, 21], [20, 23]]]

base_path = '/home/joel/DeepLearning/SLP/SLP/'

dates = ['20181024', '20181024', '20181024', '20181025', '20181025', '20181025', '20181025', '20181026',
         '20181026', '20181026', '20181027', '20181027', '20181027', '20181027', '20181027', '20181028',
         '20181028', '20181028', '20181029', '20181029', '20181029', '20181029', '20181029', '20181030']

# Loop through all models of interest
for i, input_output_combo in enumerate(list_input_output_combos):
    input_channels = input_output_combo[0]
    output_channels = input_output_combo[1]
    sess = tf.Session()
    K.set_session(sess)

    rescaling = 16

    filename_input_channels = 'Input_'
    for channel_idx in input_channels:
        filename_input_channels += channel_names[channel_idx] + '_'

    filename_input_channels += 'Predicting_' + channel_names[output_channels[0]]
    print(filename_input_channels)

    autoencoder_name = os.path.join(base_path, dates[i] + 'SLP_SubcellularLoss_Rescaling_' + str(rescaling) + '_' +
                                    filename_input_channels + '.h5')

    csv_output_name = 'TestLoss5x5_' + datetime.datetime.today().strftime('%Y%m%d') + 'SLP_SubcellularLoss_' + filename_input_channels + '.csv'


    with open(csv_output_name,'w') as fyle:
        pass

    img_size = [640, 640]
    batch_size = 16
    regex_basefile = '20180606-SLP_Multiplexing_p1_*DAPI*'
    # Load testing data
    generator = generate_testing_batch_from_path(testing_path, batch_size, regex_basefile,img_size, input_channels, output_channels, channel_names, rescaling)
    for x_test, y_test, loaded_filenames in generator:
        sess = tf.Session()
        K.set_session(sess)
        segmentations = y_test[:, :, :, 1]

        autoencoder = load_model(autoencoder_name, custom_objects={'subcellular_loss': subcellular_loss})

        decoded_imgs = autoencoder.predict(x_test).astype('float32')

        # Calculate loss on current batch
        current_loss = subcellular_loss(y_test.astype('float32'), decoded_imgs).eval(session = sess)
        loss_per_cell = zip(current_loss,loaded_filenames)

        # Write loss & filenames to csv
        with open(csv_output_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(loss_per_cell)

        K.clear_session()
