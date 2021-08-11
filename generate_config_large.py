from data import *
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from pathlib import Path


# generates random input-files based on source-files
# num_samples - how many input files (binvox) shall be generated
# num_features_min, num_features_max - how many features the generated files shall contain
#                                      (how many source-files shall be combined)
#
def create_data_set(num_samples, num_features_min, num_features_max, folder_name):
    #
    remove_old_files(folder_name)

    random.seed()  # initialize the random number generator

    list_files = create_file_dictionary_simple()

    for idx in range(num_samples):

        print(folder_name, 'processing the', idx, 'of', num_samples, 'image...')

        cur_model, \
        cur_model_label, \
        cur_model_components = achieve_random_model_simple(
            list_files,
            num_features_min,
            num_features_max,
            folder_name + str(idx) + "__"
        )

        # rotate binvox and create PNG for each side of the cube
        for rotation in range(6):

            img, _ = create_img(cur_model, rotation, True)
            target = achieve_model_gt(cur_model_label, cur_model_components, rotation)

            # skip the solid side of the cube
            if target.shape[0] == 0:
                continue

            filename = folder_name + str(idx) + str("_") + str(rotation)
            plt.imsave(filename + '.png', img, cmap='gray', vmin=0, vmax=255)

            np.save(filename + '.npy', target)


def remove_old_files(folder_name):
    files = \
        list(Path(folder_name).glob('*.binvox')) + \
        list(Path(folder_name).glob('*.binvox.txt')) + \
        list(Path(folder_name).glob('*.npy')) + \
        list(Path(folder_name).glob('*.png'))

    for single_file in files:
        os.remove(single_file)


if __name__ == '__main__':
    # medium configuration
    create_data_set(50, 2, 2, 'data/TrSet/')
    create_data_set(10, 2, 2, 'data/ValSet/')

    # large configuration
    # create_data_set(1_000_000, 2, 5, 'data/TrSet/')
    # create_data_set(1000, 2, 5, 'data/ValSet/')
