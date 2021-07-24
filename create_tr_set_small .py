from data.voc0712 import *

partition = create_partition(512, 100)
# partition = 2 dict (train/val)
list_IDs = partition['train']

# DIR = 'data/config_small/training_set/'
DIR = 'data/config_small/validation_set/'
BINVOX_DIR = 'data/config_small/binvox/'

for idxBinvox in range(100, 120):

    cur_model, cur_model_label, cur_model_components = achieve_fixed_model(
        BINVOX_DIR + "1_" + str(idxBinvox) + ".binvox")

    for rotation in range(6):

        img, _ = create_img(cur_model, rotation, True)
        target = achieve_model_gt(cur_model_label, cur_model_components, rotation)

        if target.shape[0] == 0:
            continue

        print('processing the', idxBinvox, 'th image...')
        filename = DIR + str(idxBinvox) + str("_") + str(rotation)
        plt.imsave(filename + '.png', img, cmap='gray', vmin=0, vmax=255)

        np.save(filename + '.npy', target)
