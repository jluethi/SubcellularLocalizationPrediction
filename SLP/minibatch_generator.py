import numpy as np
import cv2
import os
import glob
import re
import copy


def generate_batch_from_path(path, batch_size, regex_basefile, img_size,
                             input_channels, output_channels, channel_names, rescaling = 1):

    batch_input = np.zeros((batch_size,) + (img_size[0], img_size[1], len(input_channels)))
    batch_output = np.zeros((batch_size,) + (img_size[0], img_size[1], len(output_channels)))
    training_files_original = glob.glob(os.path.join(path, regex_basefile))
    training_files = copy.deepcopy(training_files_original)
    while True:
        # Randomly draw a batch of images and remove them from the list of images to be processed
        if len(training_files) > batch_size:
            filenames = []

            # Collect images for one batch of input/output
            for i in range(batch_size):
                index = int(np.random.choice(len(training_files), 1))
                filenames.append(training_files[index].split('/')[-1])
                # Load output
                for output_idx in range(len(output_channels)):
                    filename_channel = re.sub('2_DAPI', channel_names[output_channels[output_idx]], training_files[index])
                    img = cv2.imread(os.path.join(path, filename_channel), 0)
                    if output_idx == 0:
                        batch_output[i, :, :, output_idx] = img / 255. * rescaling
                    else:
                        batch_output[i, :, :, output_idx] = img / 255.

                # Load input
                for channel_idx in range(len(input_channels)):
                    filename_channel = re.sub('2_DAPI', channel_names[input_channels[channel_idx]], training_files[index])
                    img = cv2.imread(os.path.join(path, filename_channel), 0)
                    batch_input[i, :, :, channel_idx] = img / 255.
                    # can apply some processing here, e.g. rotation using from scipy.ndimage.interpolation import rotate

                # Remove the loaded data from the training_files
                del training_files[index]


            yield batch_input, batch_output

        # When there are not enough images left in the traing_files list to generate a batch,
        # refresh the training_files list (to the original list)
        # If each epoch uses just the correct amount of batches, it will run through every file once
        # This is currently not enforced by this function
        # TODO: Ensure that every file is used once per epoch (instead of epoch length depending on input)
        else:
            training_files = copy.deepcopy(training_files_original)


def generate_testing_batch_from_path(path, batch_size, regex_basefile, img_size, input_channels,
                                     output_channels, channel_names, rescaling = 1):

    # Batch generator to be used when evaluating a test set after having trained the model
    batch_input = np.zeros((batch_size,) + (img_size[0], img_size[1], len(input_channels)))
    batch_output = np.zeros((batch_size,) + (img_size[0], img_size[1], len(output_channels)))
    training_files_original = glob.glob(os.path.join(path, regex_basefile))
    training_files = copy.deepcopy(training_files_original)
    while len(training_files) > batch_size:
        # Randomly draw a batch of images and remove them from the list of images to be processed
        filenames = []
        to_be_removed = []

        # Collect images for one batch of input/output
        for i in range(batch_size):
            index = int(np.random.choice(len(training_files), 1))
            filenames.append(training_files[index].split('/')[-1])
            # Load output
            for output_idx in range(len(output_channels)):
                filename_channel = re.sub('2_DAPI', channel_names[output_channels[output_idx]], training_files[index])
                img = cv2.imread(os.path.join(path, filename_channel), 0)
                if output_idx == 0:
                    batch_output[i, :, :, output_idx] = img / 255. * rescaling
                else:
                    batch_output[i, :, :, output_idx] = img / 255.

            # Load input
            for channel_idx in range(len(input_channels)):
                filename_channel = re.sub('2_DAPI', channel_names[input_channels[channel_idx]], training_files[index])
                img = cv2.imread(os.path.join(path, filename_channel), 0)
                batch_input[i, :, :, channel_idx] = img / 255.
                # can apply some processing here, e.g. rotation using from scipy.ndimage.interpolation import rotate

            # Remove the loaded data from the training_files
            del training_files[index]

        yield batch_input, batch_output, filenames

    # After all full size batches have been drawn, generate a batch with all remaining images
    last_batch = len(training_files)
    batch_input = np.zeros((last_batch,) + (img_size[0], img_size[1], len(input_channels)))
    batch_output = np.zeros((last_batch,) + (img_size[0], img_size[1], len(output_channels)))
    # Randomly draw a batch of images and remove them from the list of images to be processed
    filenames = []
    to_be_removed = []

    # Collect images for one batch of input/output
    for i in range(last_batch):
        index = int(np.random.choice(len(training_files), 1))
        filenames.append(training_files[index].split('/')[-1])
        # Load output
        for output_idx in range(len(output_channels)):
            filename_channel = re.sub('2_DAPI', channel_names[output_channels[output_idx]], training_files[index])
            img = cv2.imread(os.path.join(path, filename_channel), 0)
            if output_idx == 0:
                batch_output[i, :, :, output_idx] = img / 255. * rescaling
            else:
                batch_output[i, :, :, output_idx] = img / 255.

        # Load input
        for channel_idx in range(len(input_channels)):
            filename_channel = re.sub('2_DAPI', channel_names[input_channels[channel_idx]], training_files[index])
            img = cv2.imread(os.path.join(path, filename_channel), 0)
            batch_input[i, :, :, channel_idx] = img / 255.
            # can apply some processing here, e.g. rotation using from scipy.ndimage.interpolation import rotate

        # Remove the loaded data from the training_files
        del training_files[index]

    yield batch_input, batch_output, filenames


def generate_deterministic_testing_batch_from_path(path, batch_size, regex_basefile, img_size, input_channels,
                                     output_channels, channel_names, rescaling = 1):

    # Batch generator to be used when evaluating a test set after having trained the model
    batch_input = np.zeros((batch_size,) + (img_size[0], img_size[1], len(input_channels)))
    batch_output = np.zeros((batch_size,) + (img_size[0], img_size[1], len(output_channels)))
    training_files_original = glob.glob(os.path.join(path, regex_basefile))
    training_files = copy.deepcopy(training_files_original)
    index = 0
    while len(training_files) > batch_size:
        # Randomly draw a batch of images and remove them from the list of images to be processed
        filenames = []
        to_be_removed = []

        # Collect images for one batch of input/output
        for i in range(batch_size):
            filenames.append(training_files[index].split('/')[-1])
            # Load output
            for output_idx in range(len(output_channels)):
                filename_channel = re.sub('2_DAPI', channel_names[output_channels[output_idx]], training_files[index])
                img = cv2.imread(os.path.join(path, filename_channel), 0)
                if output_idx == 0:
                    batch_output[i, :, :, output_idx] = img / 255. * rescaling
                else:
                    batch_output[i, :, :, output_idx] = img / 255.

            # Load input
            for channel_idx in range(len(input_channels)):
                filename_channel = re.sub('2_DAPI', channel_names[input_channels[channel_idx]], training_files[index])
                img = cv2.imread(os.path.join(path, filename_channel), 0)
                batch_input[i, :, :, channel_idx] = img / 255.
                # can apply some processing here, e.g. rotation using from scipy.ndimage.interpolation import rotate

            # Remove the loaded data from the training_files
            del training_files[index]

        yield batch_input, batch_output, filenames

    # After all full size batches have been drawn, generate a batch with all remaining images
    last_batch = len(training_files)
    batch_input = np.zeros((last_batch,) + (img_size[0], img_size[1], len(input_channels)))
    batch_output = np.zeros((last_batch,) + (img_size[0], img_size[1], len(output_channels)))
    # Randomly draw a batch of images and remove them from the list of images to be processed
    filenames = []
    to_be_removed = []

    # Collect images for one batch of input/output
    for i in range(last_batch):
        filenames.append(training_files[index].split('/')[-1])
        # Load output
        for output_idx in range(len(output_channels)):
            filename_channel = re.sub('DAPI', channel_names[output_channels[output_idx]], training_files[index])
            img = cv2.imread(os.path.join(path, filename_channel), 0)
            if output_idx == 0:
                batch_output[i, :, :, output_idx] = img / 255. * rescaling
            else:
                batch_output[i, :, :, output_idx] = img / 255.

        # Load input
        for channel_idx in range(len(input_channels)):
            filename_channel = re.sub('DAPI', channel_names[input_channels[channel_idx]], training_files[index])
            img = cv2.imread(os.path.join(path, filename_channel), 0)
            batch_input[i, :, :, channel_idx] = img / 255.
            # can apply some processing here, e.g. rotation using from scipy.ndimage.interpolation import rotate

        # Remove the loaded data from the training_files
        del training_files[index]

    yield batch_input, batch_output, filenames
