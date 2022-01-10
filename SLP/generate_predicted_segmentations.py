from keras.models import load_model
import numpy as np
# import matplotlib.pyplot as plt
import cv2
import os
import glob
import re
from custom_loss_functions import weighted_crossentropy
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

list_input_output_combos = [[[0], [7, 23]], [[0, 6], [7, 23]], [[0, 8], [7, 23]], [[0, 13], [7, 23]],
                            [[0, 19], [7, 23]], [[0, 13, 19], [7, 23]], [[0, 2, 18, 19], [7, 23]],
                            [[0, 2, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], [7, 23]]]
train_date = ['20180907', '20180907', '20180908', '20180908', '20180908', '20180908', '20180908', '20180908', '20180908']

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
    autoencoder_name = train_date[i] + 'SLP_SubcellularSegmentationLoss_10xWeights_' + filename_input_channels + '.h5'
    output_path = '/home/joel/DeepLearning/20180502_SLP_Experiment/PredictionsSegmentation_' + \
                  datetime.datetime.today().strftime('%Y%m%d') + '_' + filename_input_channels + '/'
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    img_size = [640, 640]
    batch_size = 8
    regex_basefile = '20180606-SLP_Multiplexing_p1_*DAPI*'
    rescaling = 1
    prediction_rounds = 25

    # Load testing data
    generator = generate_deterministic_testing_batch_from_path(testing_path, batch_size, regex_basefile,img_size, input_channels, output_channels, channel_names, rescaling)

    for j in range(prediction_rounds):
        [x_test, y_test, loaded_filenames] = generator.next()
        segmentations = y_test[:, :, :, 1]

        autoencoder = load_model(autoencoder_name, custom_objects={'weighted_crossentropy': weighted_crossentropy})

        decoded_imgs = autoencoder.predict(x_test).astype('float32')


        # Save images to disk
        print('Saving images')

        for i in range(batch_size):
            output_img = decoded_imgs[i, :, :, 1] * 255 / rescaling
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
