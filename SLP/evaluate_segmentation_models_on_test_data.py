from keras.models import load_model
# import numpy as np
# import matplotlib.pyplot as plt
import os
from minibatch_generator import generate_testing_batch_from_path
from keras import backend as K
import tensorflow as tf
import csv
import datetime
from custom_loss_functions import weighted_crossentropy_evaluation

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

inputs_of_interest = [[0], [0, 6], [0, 8], [0, 13], [0, 19], [0, 13, 19], [0, 2, 18, 19],
                      [0, 2, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]]

output_channels = [7, 23]
base_path = ['/home/joel/DeepLearning/SLP/SLP/',
             '/home/joel/DeepLearning/SLP/SLP/',
             '/home/joel/DeepLearning/SLP/SLP/',
             '/home/joel/DeepLearning/SLP/SLP/',
             '/home/joel/DeepLearning/SLP/SLP/',
             '/home/joel/DeepLearning/SLP/SLP/',
             '/home/joel/DeepLearning/SLP/SLP/',
             '/home/joel/DeepLearning/SLP/SLP/']

rescaling_list = [1, 1, 1, 1, 1, 1, 1, 1]
train_date = ['20180907', '20180907', '20180908', '20180908', '20180908', '20180908', '20180908', '20180908', '20180908']

# Loop through all models of interest
for i, input_channels in enumerate(inputs_of_interest):
    sess = tf.Session()
    K.set_session(sess)

    rescaling = rescaling_list[i]

    filename_input_channels = 'Input_'
    for channel_idx in input_channels:
        filename_input_channels += channel_names[channel_idx] + '_'

    filename_input_channels += 'Predicting_' + channel_names[output_channels[0]]
    print(filename_input_channels)

    autoencoder_name = os.path.join(base_path[i], train_date[i] + '_SLP_SubcellularSegmentationLoss_10xWeights_' +
                                    filename_input_channels + '.h5')

    csv_output_name = 'TestLoss_' + datetime.datetime.today().strftime('%Y%m%d') + \
                      'SLP_SubcellularSegmentationLoss_10xWeights_' + filename_input_channels + '.csv'

    with open(csv_output_name,'w') as fyle:
        pass

    img_size = [640, 640]
    batch_size = 1
    regex_basefile = '20180606-SLP_Multiplexing_p1_*DAPI*'
    # Load testing data
    generator = generate_testing_batch_from_path(testing_path, batch_size, regex_basefile, img_size, input_channels,
                                                 output_channels, channel_names, rescaling)
    for x_test, y_test, loaded_filenames in generator:
        sess = tf.Session()
        K.set_session(sess)

        autoencoder = load_model(autoencoder_name, custom_objects={'weighted_crossentropy': weighted_crossentropy_evaluation})

        decoded_imgs = autoencoder.predict(x_test).astype('float32')

        # Calculate loss on current batch
        current_loss = weighted_crossentropy_evaluation(y_test.astype('float32'), decoded_imgs).eval(session = sess)
        loss_per_cell = [current_loss,loaded_filenames[0]]

        # Write loss & filenames to csv
        with open(csv_output_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(loss_per_cell)

        K.clear_session()
