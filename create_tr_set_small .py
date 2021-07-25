from data.voc0712 import *


def create_training_set():
    create_files('data/config_small/training_set/', 0, 99)


def create_validation_set():
    create_files('data/config_small/validation_set/', 100, 119)


def create_files(targetDir, idxFirst, idxLast):
    BINVOX_DIR = 'data/config_small/binvox/'

    for idxBinvox in range(idxFirst, idxLast+1):

        cur_model, cur_model_label, cur_model_components = achieve_fixed_model(BINVOX_DIR + "1_" + str(idxBinvox) + ".binvox")

        for rotation in range(6):

            img, _ = create_img(cur_model, rotation, True)
            target = achieve_model_gt(cur_model_label, cur_model_components, rotation)

            if target.shape[0] == 0:
                continue

            print('processing the', idxBinvox, 'th image...')
            filename = targetDir + str(idxBinvox) + str("_") + str(rotation)
            plt.imsave(filename + '.png', img, cmap='gray', vmin=0, vmax=255)

            np.save(filename + '.npy', target)


def achieve_fixed_model(filename):
    label = int(os.path.basename(filename).split('_')[0])
    model_label = np.zeros(0)
    model_label = np.append(model_label, label)
    with open(filename, 'rb') as f:
        model = utils.binvox_rw.read_as_3d_array(f).data

    components = np.zeros((1, 64, 64, 64))
    components[0, :, :, :] = model

    return model, model_label, components


if __name__ == '__main__':
    create_training_set()
    create_validation_set()
