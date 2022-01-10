from keras.models import Model
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, concatenate
from keras.layers.normalization import BatchNormalization
import numpy as np
from keras.callbacks import TensorBoard
# import cv2
# import os
# import re
# import glob
from custom_loss_functions import subcellular_loss
from minibatch_generator import generate_batch_from_path


def train_UNet(input_channels, output_channel):
    ##################################
    # General parameters
    ##################################
    batch_size = 8
    nbEpochs = 150

    channel_names = ['2_DAPI', '10_Paxillin', '10_Pericentrin', '11_EEA1', '11_Sara', '13_DCP1a',
                     '13_DDX6', '13_Pbody_Segm', '13_Succs', '1_Lamp1', '1_PCNA',
                     '2_Calreticulin', '3_APPL', '3_GM130', '4_HSP60',
                     '4_LC3B', '5_pS6', '5_Yap', '7_Acetyl_Tubulin', '7_Actin',
                     '8_Caveolin', '8_Pol2', '9_ABCD3', 'segmentation']

    rescaling = 32

    nbChannels = len(input_channels)

    img_size = [640, 640]

    input_img = Input(shape=(img_size[0], img_size[1], nbChannels))

    # Only select control wells: Columns 3 - 6
    regex_basefile = '20180606-SLP_Multiplexing_p1_*DAPI*'

    # File paths
    validation_path = '/home/joel/DeepLearning/20180502_SLP_Experiment/singleCellImages_dividedDatasets/validation'
    training_path = '/home/joel/DeepLearning/20180502_SLP_Experiment/singleCellImages_dividedDatasets/train'

    # Output filenames
    filename_input_channels = ''
    for channel_idx in input_channels:
        filename_input_channels += channel_names[channel_idx] + '_'

    filename_base = 'SLP_SubcellularLoss_Input_' + filename_input_channels + 'Predicting_' + channel_names[
        output_channel[0]]

    ##################################
    # Define model
    ##################################

    # Encoder
    # First encoder layer: 640x640
    encode1 = BatchNormalization(axis=-1, name='BatchN_Layer1_1')(input_img)
    encode1 = Conv2D(16, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer1_1')(encode1)
    encode1 = BatchNormalization(axis=-1, name='BatchN_Layer1_2')(encode1)
    encode1 = Conv2D(16, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer1_2')(encode1)
    encode1 = BatchNormalization(axis=-1, name='BatchN_Layer1_3')(encode1)
    encode1 = Conv2D(16, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer1_3')(encode1)

    # Second encoder layer: 320x320
    encode2 = MaxPooling2D((2, 2), padding='same', name='Maxpool_Layer2')(encode1)
    encode2 = BatchNormalization(axis=-1, name='BatchN_Layer2_1')(encode2)
    encode2 = Conv2D(32, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer2_1')(encode2)
    encode2 = BatchNormalization(axis=-1, name='BatchN_Layer2_2')(encode2)
    encode2 = Conv2D(32, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer2_2')(encode2)

    # Third encoder layer: 160x160
    encode3 = MaxPooling2D((2, 2), padding='same', name='Maxpool_Layer3')(encode2)
    encode3 = BatchNormalization(axis=-1, name='BatchN_Layer3_1')(encode3)
    encode3 = Conv2D(64, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer3_1')(encode3)
    encode3 = BatchNormalization(axis=-1, name='BatchN_Layer3_2')(encode3)
    encode3 = Conv2D(64, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer3_2')(encode3)

    # Fourth encoder layer: 80x80
    encode4 = MaxPooling2D((2, 2), padding='same', name='Maxpool_Layer4')(encode3)
    encode4 = BatchNormalization(axis=-1, name='BatchN_Layer4_1')(encode4)
    encode4 = Conv2D(128, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer4_1')(encode4)
    encode4 = BatchNormalization(axis=-1, name='BatchN_Layer4_2')(encode4)
    encode4 = Conv2D(128, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer4_2')(encode4)

    # Fifth encoder layer: 40x40
    encode5 = MaxPooling2D((2, 2), padding='same', name='Maxpool_Layer5')(encode4)
    encode5 = BatchNormalization(axis=-1, name='BatchN_Layer5_1')(encode5)
    encode5 = Conv2D(256, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer5_1')(encode5)
    encode5 = BatchNormalization(axis=-1, name='BatchN_Layer5_2')(encode5)
    encode5 = Conv2D(256, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer5_2')(encode5)
    encode5 = BatchNormalization(axis=-1, name='BatchN_Layer5_3')(encode5)
    encode_5 = Conv2D(512, (3, 3), activation='relu', padding='same', name='Conv2D_Encode_Layer5_3')(encode5)

    # Decoder
    # Fifth Decoder layer 40x40
    encode5 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer5_1')(encode5)
    decode_5 = Conv2D(256, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer5_1')(encode_5)

    # Fourth decoder layer 80x80
    decode_4 = concatenate([encode4, UpSampling2D((2, 2))(decode_5)], name='Concatenate_Layer4')
    decode_4 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer4_1')(decode_4)
    decode_4 = Conv2D(128, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer4_1')(decode_4)
    decode_4 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer4_2')(decode_4)
    decode_4 = Conv2D(128, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer4_2')(decode_4)

    # Third decoder layer 160x160
    decode_3 = concatenate([encode3, UpSampling2D((2, 2))(decode_4)], name='Concatenate_Layer3')
    decode_3 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer3_1')(decode_3)
    decode_3 = Conv2D(64, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer3_1')(decode_3)
    decode_3 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer3_2')(decode_3)
    decode_3 = Conv2D(64, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer3_2')(decode_3)

    # Second decoder layer 320x320
    decode_2 = concatenate([encode2, UpSampling2D((2, 2))(decode_3)], name='Concatenate_Layer2')
    decode_2 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer2_1')(decode_2)
    decode_2 = Conv2D(32, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer2_1')(decode_2)
    decode_2 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer2_2')(decode_2)
    decode_2 = Conv2D(32, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer2_2')(decode_2)

    # Second decoder layer 640x640
    decode_1 = concatenate([encode1, UpSampling2D((2, 2))(decode_2)], name='Concatenate_Layer1')
    decode_1 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer1_1')(decode_1)
    decode_1 = Conv2D(16, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer1_1')(decode_1)
    decode_1 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer1_2')(decode_1)
    decode_1 = Conv2D(16, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer1_2')(decode_1)
    decode_1 = BatchNormalization(axis=-1, name='BatchN_Decode_Layer1_3')(decode_1)
    decoded = Conv2D(1, (3, 3), activation='relu', padding='same', name='Conv2D_Decode_Layer1_3')(decode_1)

    autoencoder = Model(input_img, decoded)
    # sgd = optimizers.SGD(lr = 0.005, decay = 0.0, momentum = 0.0, nesterov = False)
    autoencoder.compile(optimizer='adam', loss=subcellular_loss)  # 'mse', optimizer='adadelta'

    steps_per_epoch = 200
    callback_list = [
        ModelCheckpoint(filename_base + '_autosave.h5', monitor='val_loss', verbose=1, period=1, save_best_only=True),
        TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=32, write_graph=True)]

    autoencoder.fit_generator(generate_batch_from_path(training_path, batch_size, regex_basefile, img_size,
                                                       input_channels, output_channel, channel_names, rescaling),
                              steps_per_epoch=steps_per_epoch,
                              validation_data=generate_batch_from_path(
                                  validation_path, batch_size, regex_basefile, img_size, input_channels, output_channel,
                                  channel_names, rescaling), validation_steps=20, callbacks=callback_list,
                              epochs=nbEpochs)

    autoencoder.save(filename_base + '.h5')
