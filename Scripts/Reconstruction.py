import os
import pickle
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join


def Reconstruct(perc):
    path = "Output\sliced_and_resized"
    predictions_raw = pd.read_pickle(path + "/predictions.pickle")

    predictions_raw = np.delete(predictions_raw, np.where(predictions_raw[:, 7] <= perc)[0], axis=0)

    first_subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    onlyfiles = []
    paths = []
    HD_images = []
    HD_location = "Output\HD_pictures"
    HDfiles = [HD_location + "/" + f for f in listdir(HD_location) if isfile(join(HD_location, f))]

    for image in HDfiles:
        image = Image.open(image)
        image = np.array(image)
        HD_images.append(image)

    for x in first_subfolders:
        path_dim = [f.path for f in os.scandir(x) if f.is_dir()]
        paths = paths + path_dim

    for itr in range(len(paths)):
        path = paths[itr]
        onlyfiles.extend([path + "/" + f for f in listdir(path) if isfile(join(path, f))])

    for prediction in predictions_raw:
        picture_index = int(prediction[8])
        #print(picture_index)
        mini_picture = onlyfiles[picture_index]
        mini_name = mini_picture.split("/")[-1].split("_")        #get hd picture
        HD_LOC = "Output\HD_pictures/HD_" + str(mini_name[0]) + "_" + str(mini_name[1]) + "_" + str(mini_name[2]) + ".png"
        HD_index =  HDfiles.index(HD_LOC)






        max_x_dim = HD_images[HD_index].shape[0]
        max_y_dim = HD_images[HD_index].shape[1]
        rec_scale = int(mini_name[-1].replace(".png", ""))
        scaler = rec_scale/64

        startposition_x = int(mini_name[-3])
        startposition_y = int(mini_name[-2])

        z1 = int(prediction[0] * scaler * 64)
        x1 = int(prediction[1] * scaler * 64) + startposition_x
        y1 = int(prediction[2] * scaler * 64) + startposition_y
        z2 = (int(prediction[3] * scaler * 64) - 1)
        x2 = (int(prediction[4] * scaler * 64) + startposition_x - 1)
        y2 = (int(prediction[5] * scaler * 64) + startposition_y - 1)
        Feature = prediction[6]
        prop = prediction[7]

        if x2>=max_x_dim:
            x2 = max_x_dim-1
        if y2>=max_y_dim:
            y2 = max_y_dim-1

        if x1>=max_x_dim or y1 >=max_y_dim or x1>=x2 or y1>=y2:
            continue


        color = {
            0: [255, 255, 0, 255],
            1: [255, 0, 0, 255],
            2: [0, 255, 0, 255],
            3: [0, 0, 255, 255],
            4: [255, 127, 0, 255],
            5: [255, 212, 0, 255],
            6: [255, 255, 0, 255],
            7: [191, 255, 0, 255],
            8: [106, 255, 0, 255],
            9: [0, 234, 255, 255],
            10: [0, 149, 255, 255],
            11: [0, 64, 255, 255],
            12: [170, 0, 255, 255],
            13: [255, 0, 170, 255],
            14: [237, 185, 185, 255],
            15: [231, 233, 185, 255],
            16: [185, 237, 224, 255],
            17: [185, 215, 237, 255],
            18: [220, 185, 237, 255],
            19: [143, 35, 35, 255],
            20: [143, 106, 3, 255],
            21: [79, 143, 35, 255],
            22: [35, 98, 143, 255],
            23: [107, 35, 143, 255],
            24: [115, 115, 115, 255],
            25: [204, 204, 204, 255]
        }[Feature]

        color = np.asarray(color[0:3][::-1])
        HD_images[HD_index][x1][y1] = color
        HD_images[HD_index][x2][y2] = color

        for x in range(x2 - x1):
            HD_images[HD_index][x1 + x][y1] = color
            HD_images[HD_index][x1 + x][y2] = color

        for x in range(y2 - y1):
            HD_images[HD_index][x1][y1 + x] = color
            HD_images[HD_index][x2][y1 + x] = color


    for idx, x in enumerate(HD_images):
        HD_picture_save = Image.fromarray(x)
        HD_picture_save.save("Output/" + str(idx) +".png")
