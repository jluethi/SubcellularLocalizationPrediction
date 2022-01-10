# Script to define a custom loss function for comparing original images with predicted images
from keras import backend as K
import numpy as np
import tensorflow as tf

def subcellular_loss(input, predicted_image):
    # Implements a MSE loss limited to the inside of the cell.
    # The segmentation is always the second part in z of the original image
    # https://github.com/fchollet/keras/issues/7065
    original_image = K.expand_dims(input[:, :, :, 0], axis=-1)
    segmentation_image = K.cast(K.expand_dims(input[:, :, :, 1], axis=-1), K.floatx())
    masked_squared_error = K.square(segmentation_image * (original_image - predicted_image))
    masked_mse = K.sum(K.sum(K.sum(masked_squared_error, axis=-1), axis=-1), axis=-1) \
                 / K.sum(K.sum(K.sum(segmentation_image, axis=-1), axis=-1), axis=-1)
    return masked_mse


# def subcellular_intNorm_loss(input, predicted_image):
#     # Implements a MSE loss limited to the inside of the cell.
#     # The segmentation is always the second part in z of the original image
#     # https://github.com/fchollet/keras/issues/7065
#     # Additionally does a loss normalization, not sure if it is helpful
#     original_image = K.expand_dims(input[:,:,:,0], axis = -1)
#     segmentation_image = K.cast(K.expand_dims(input[:,:,:,1], axis = -1), K.floatx())
#     masked_squared_error = K.square(segmentation_image*(original_image-predicted_image))
#     masked_mse = K.sum(K.sum(K.sum(masked_squared_error, axis = -1), axis = -1), axis = -1)
#                   / K.sum(K.sum(K.sum(segmentation_image, axis = -1), axis = -1), axis = -1)
#
#     mean_int_original = K.sum(K.sum(K.sum(segmentation_image * original_image, axis = -1), axis = -1), axis = -1)
#     mean_int_predicted = K.sum(K.sum(K.sum(segmentation_image * predicted_image, axis=-1), axis=-1), axis=-1)
#     int_diff_percentage = abs(mean_int_original - mean_int_predicted) / mean_int_original
#     return (int_diff_percentage + masked_mse) / 2

def binary_to_onehot(binary_image):
    # Function that transforms the P body segmentation image of the form [batch_size, x, y, 1] to
    # [batch_size, x, y, 2], where the last dimension is onehot encoded segmentation information
    # [batch_size, x, y, 0] 1 for all background pixels and 0 for all P body pixels
    # [batch_size, x, y, 1] 0 for all background pixels and 1 for all P body pixels
    output_list = []
    output_list.append(K.equal(binary_image, K.zeros(shape=(8, 640, 640))))
    output_list.append(K.equal(binary_image, K.ones(shape=(8, 640, 640))))
    # output_list.append(K.equal(binary_image, K.zeros(shape=(1, 4, 4))))
    # output_list.append(K.equal(binary_image, K.ones(shape=(1, 4, 4))))
    onehot_image = K.stack(output_list, axis = -1)
    return K.cast(onehot_image, K.floatx())

# example = K.zeros(shape=(8,640,640))
# print(binary_to_onehot(example))


def weighted_crossentropy(input_image, predicted_image):
    # Implements a softmax crossvalidated loss similar to the implementation in the 2015 UNET paper
    # Scales to balance classes: P bodies are less than 1% of cell area => force network to value them the same as background
    #scale_background = 1.0099
    #scale_foreground = 102.015
    scale_background = 1.0
    scale_foreground = 10.0

    original_image = input_image[:, :, :, 0]
    onehot_image = binary_to_onehot(original_image)
    segmentation_image = K.cast(input_image[:, :, :, 1], K.floatx())
    groundtruth_background = tf.scalar_mul(tf.to_float(scale_background), onehot_image[:, :, :, 0])
    groundtruth_foreground = tf.scalar_mul(tf.to_float(scale_foreground), onehot_image[:, :, :, 1])
    # tf.scalar_mul(onehot_image[:, :, :, 1], tf.to_float(0.01))

    pixel_losses = - (groundtruth_background * K.log(predicted_image[:, :, :, 0]) + groundtruth_foreground * K.log(predicted_image[:, :, :, 1]))

    # Scale the loss by the size of the cell (otherwise small cells have smaller losses)
    weighted_loss = K.sum(K.sum(K.sum(segmentation_image * pixel_losses, axis=-1), axis=-1), axis=-1) /\
                    K.sum(K.sum(K.sum(segmentation_image, axis=-1), axis=-1), axis=-1)
    return weighted_loss


def weighted_crossentropy_evaluation(input_image, predicted_image):
    # Implements a softmax crossvalidated loss similar to the implementation in the 2015 UNET paper
    # Scales to balance classes: P bodies are less than 1% of cell area => force network to value them the same as background
    #scale_background = 1.0099
    #scale_foreground = 102.015
    scale_background = 1.0
    scale_foreground = 10.0

    original_image = input_image[:, :, :, 0]
    output_list = []
    output_list.append(K.equal(original_image, K.zeros(shape=(8, 640, 640)).initialized_value()))
    output_list.append(K.equal(original_image, K.ones(shape=(8, 640, 640)).initialized_value()))
    onehot_image_tmp = K.stack(output_list, axis=-1)
    onehot_image = K.cast(onehot_image_tmp, K.floatx())

    segmentation_image = K.cast(input_image[:, :, :, 1], K.floatx())
    groundtruth_background = tf.scalar_mul(tf.to_float(scale_background), onehot_image[:, :, :, 0])
    groundtruth_foreground = tf.scalar_mul(tf.to_float(scale_foreground), onehot_image[:, :, :, 1])
    # tf.scalar_mul(onehot_image[:, :, :, 1], tf.to_float(0.01))

    pixel_losses = - (groundtruth_background * K.log(predicted_image[:, :, :, 0]) + groundtruth_foreground * K.log(predicted_image[:, :, :, 1]))

    # Scale the loss by the size of the cell (otherwise small cells have smaller losses)
    weighted_loss = K.sum(K.sum(K.sum(segmentation_image * pixel_losses, axis=-1), axis=-1), axis=-1) /\
                    K.sum(K.sum(K.sum(segmentation_image, axis=-1), axis=-1), axis=-1)
    return weighted_loss


# # example1 = K.ones(shape=(1,4,4,2))
# weights = tf.constant([1.01, 100])
# # Row 1) Background, predicted foreground
# # Row 2) Background, predicted background
# # Row 3) Foreground, predicted backgroung
# # Row 4) Foreground, predicted foreground
# example1 = tf.constant([[[[0.0, 0.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]], [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]],
#                          [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]]])
#
# example2 = tf.constant([[[[0.01, 0.99], [0.01, 0.99], [0.01, 0.99], [0.01, 0.99]], [[0.99, 0.01], [0.99, 0.01], [0.99, 0.01], [0.99, 0.01]],
#                          [[0.99, 0.01], [0.99, 0.01], [0.99, 0.01], [0.99, 0.01]], [[0.01, 0.99], [0.01, 0.99], [0.01, 0.99], [0.01, 0.99]]]])
#
#
# sess = tf.Session()
# K.set_session(sess)
#
# # print(example1.eval())
# a = weighted_crossentropy(example1, example2)
#
# tf.initialize_all_variables().run(session= sess)
# print(sess.run(example1))
# print(sess.run(example2))
# print(sess.run(a))
