from keras.models import load_model
import numpy as np
# import matplotlib.pyplot as plt
import cv2
import os
import glob
import re
from custom_loss_functions import subcellular_loss
from minibatch_generator import generate_testing_batch_from_path, generate_deterministic_testing_batch_from_path
from keras import backend as K
import tensorflow as tf
import datetime


#sess = tf.Session()
#K.set_session(sess)

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

dates = ['20181024', '20181024', '20181024', '20181025', '20181025', '20181025', '20181025', '20181026',
         '20181026', '20181026', '20181027', '20181027', '20181027', '20181027', '20181027', '20181028',
         '20181028', '20181028', '20181029', '20181029', '20181029', '20181029', '20181029', '20181030']

rescaling = 16

for i, combo in enumerate(list_input_output_combos):
    sess = tf.Session()
    K.set_session(sess)
    input_channels = combo[0]
    output_channels = combo[1]
    filename_input_channels = 'Input_'
    for channel_idx in input_channels:
        filename_input_channels += channel_names[channel_idx] + '_'

    filename_input_channels += 'Predicting_' + channel_names[output_channels[0]]
    print(filename_input_channels)
    autoencoder_name = dates[i] + 'SLP_SubcellularLoss_Rescaling_' + str(rescaling) + '_' + filename_input_channels + '.h5'
    output_path = '/home/joel/DeepLearning/20180502_SLP_Experiment/Predictions_' + dates[i] + '_' + filename_input_channels + '/'
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    img_size = [640, 640]
    batch_size = 8
    regex_basefile = '20180606-SLP_Multiplexing_p1_*DAPI*'
    prediction_rounds = 25

    # Load testing data
    # generator = generate_testing_batch_from_path(testing_path, batch_size, regex_basefile,img_size, input_channels, output_channels, channel_names, rescaling)
    generator = generate_deterministic_testing_batch_from_path(testing_path, batch_size, regex_basefile,img_size, input_channels, output_channels, channel_names, rescaling)

    for j in range(prediction_rounds):
        [x_test, y_test, loaded_filenames] = generator.next()
        segmentations = y_test[:, :, :, 1]

        autoencoder = load_model(autoencoder_name, custom_objects={'subcellular_loss': subcellular_loss})

        decoded_imgs = autoencoder.predict(x_test).astype('float32')


        # Save images to disk
        print('Saving images')

        for i in range(batch_size):
            output_img = decoded_imgs[i, :, :, 0] * 255 / rescaling
            # Mask everything outside of the segmentation
            output_img_masked = output_img * y_test[i, :, :, 1]
            output_name = output_path + loaded_filenames[i][:-4] + '_predicted_' + str(
                channel_names[output_channels[0]]) + '.png'
            cv2.imwrite(output_name, output_img_masked)

            # Also save the corresponding inputs & the original target image
            for channel_id in range(len(input_channels)):
                input_img = x_test[i, :, :, channel_id] * 255
                input_name = output_path + loaded_filenames[i][:-4] + '_input_' + str(
                    channel_names[input_channels[channel_id]]) + '.png'
                cv2.imwrite(input_name, input_img)

            original_img = y_test[i, :, :, 0] * 255 / rescaling
            original_name = output_path + loaded_filenames[i][:-4] + '_original_' + str(
                channel_names[output_channels[0]]) + '.png'
            cv2.imwrite(original_name, original_img)

            # Export the segmentation (only the outer part)
            kernel = np.ones((3, 3), np.uint8)
            segmentation_outline = cv2.morphologyEx(y_test[i, :, :, 1], cv2.MORPH_GRADIENT, kernel) * 255
            output_name = output_path + loaded_filenames[i][:-4] + 'Segmentation' + '.png'
            cv2.imwrite(output_name, segmentation_outline)
    K.clear_session()
