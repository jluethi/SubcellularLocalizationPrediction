from train_UNet_changedArchitecture import train_UNet_large_kernel

# inputs_channels: List of channels used to make a prediction
# output channels: List of two channels: First the channel to be predicted, than the segmentation image


# DDX6 prediction
# inputs_of_interest =[[0,2,10,11,13,14,16,17,18,19,21,22],
#                      [0, 2, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],[0,5]]
# inputs_of_interest = [[0, 11, 14, 18, 19]]
# inputs_of_interest = [[0], [0, 8], [0, 2, 10, 11, 13, 14, 16, 17, 18, 19, 21, 22]]
# output = [6,23]
#
# for input_channels in inputs_of_interest:
#     train_UNet_large_kernel(input_channels, output)

# P body segmentation prediction
# inputs_of_interest =[[0,8], [0,3,4,9,12,15,20], [0,2,8,10,11,13,14,16,17,18,19,21,22],
#                      [0, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],[0,5]]
# output = [7,23]

# for input_channels in inputs_of_interest:
#    train_UNet(input_channels, output)


# ABCD3 prediction
# inputs_of_interest = [[0, 4, 11], [0, 3, 4, 9, 11, 12, 15, 20], [3, 4, 9, 11, 12, 15, 20], [0, 13, 14, 18, 19],
#                       [0, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]]

# inputs_of_interest = [[0, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]]
# output = [22,23]
#
# for input_channels in inputs_of_interest:
#     train_UNet_large_kernel(input_channels, output)


# Predictions based on Succs
# input_channels = [0, 8]
# outputs_of_interest = [[2, 23], [3, 23], [9, 23], [10, 23], [11, 23], [12, 23], [13, 23], [14, 23], [18, 23],
#                        [19, 23], [20, 23], [22, 23]]
#
# for output in outputs_of_interest:
#     train_UNet(input_channels, output)


# Endocytosis prediction
# EEA1
inputs_of_interest = [[0], [0, 13], [0, 9], [0, 11], [0, 14], [0, 20], [0, 21], [0,2,10,11,13,14,16,17,18,19,21,22],
                      [0, 9, 11, 13, 14, 20, 21]]
output = [3, 23]

for input_channels in inputs_of_interest:
    train_UNet_large_kernel(input_channels, output)

# Lamp1
inputs_of_interest = [[0], [0, 13], [0, 3], [0, 11], [0, 14], [0, 20], [0, 21], [0,2,10,11,13,14,16,17,18,19,21,22],
                      [0, 3, 11, 13, 14, 20, 21]]
output = [9, 23]

for input_channels in inputs_of_interest:
    train_UNet_large_kernel(input_channels, output)

# Caveolin
inputs_of_interest = [[0], [0, 13], [0, 3], [0, 11], [0, 14], [0, 9], [0, 21], [0,2,10,11,13,14,16,17,18,19,21,22],
                      [0, 3, 9, 11, 13, 14, 21]]
output = [20, 23]

for input_channels in inputs_of_interest:
    train_UNet_large_kernel(input_channels, output)