import os
import pickle
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
import numpy as np

def Reconstruct():
    path = "Output\sliced_IS_resized"
    first_subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    #print(first_subfolders)

    for idx, x in enumerate(first_subfolders):
        second_subfolders = [f.path for f in os.scandir(x) if f.is_dir()]
        #print(second_subfolders)

        first = True
        for sec_folder in second_subfolders:
            print("reconstructing in path " + str(sec_folder) )
            predictions_raw = pd.read_pickle(sec_folder + "/predictions.pickle")
            list_of_input_pictures = [f.name for f in os.scandir(sec_folder) if f.is_file()]
            list_of_input_pictures.remove("predictions.pickle")

            if predictions_raw.size:
                #print(predictions_raw)
                temp = sec_folder.split("\\")[-1].split("_")
                name = "Output\HD_pictures\HD_" + temp[0] + "_" + temp[1] + "_" + temp[2] + ".png"

                if first:
                    HD_picture = np.array(Image.open(name))
                    first = False


                max_x_dim = HD_picture.shape[0]
                max_y_dim = HD_picture.shape[1]
                original_scale = max(max_y_dim, max_x_dim)
                rec_scale = int(temp[-1])
                scaler = rec_scale/64
                leftover = max(max_y_dim, max_x_dim) - min(max_y_dim, max_x_dim)


                if  max_x_dim<max_y_dim :
                    to_append = np.asarray([[[255, 255, 255] for x in range(max_y_dim)] for y in range(leftover)])
                    HD_picture = np.append(HD_picture, to_append, axis=0)
                    HD_picture = HD_picture.astype(np.uint8)


                for prediction in predictions_raw:
                    picture = int(prediction[8])
                    file = list_of_input_pictures[picture]
                    startposition_x = int(file.split("_")[3])
                    startposition_y = int(file.split("_")[4])

                    z1 = int(prediction[0] * scaler * 64)
                    x1 = int(prediction[1] * scaler * 64) + startposition_x
                    y1 = int(prediction[2] * scaler * 64) + startposition_y
                    z2 = (int(prediction[3] * scaler * 64) - 1)
                    x2 = (int(prediction[4] * scaler * 64) + startposition_x - 1)
                    y2 = (int(prediction[5] * scaler * 64) + startposition_y - 1)
                    Feature = prediction[6]
                    prop = prediction[7]



                    if prop>0.50:

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
                        HD_picture[x1][y1] = color
                        HD_picture[x2][y2] = color

                        for x in range(x2 - x1):
                            HD_picture[x1 + x][y1] = color
                            HD_picture[x1 + x][y2] = color

                        for x in range(y2 - y1):
                            HD_picture[x1][y1 + x] = color
                            HD_picture[x2][y1 + x] = color


                HD_picture_save = Image.fromarray(HD_picture)
                HD_picture_save.save("Output/" + str(idx) +".png")
