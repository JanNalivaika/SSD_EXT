import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
import pickle
from PIL import Image
from os import listdir
from os.path import isfile, join
import os

def Visualize():
    """#[a, b, c, d, e, f, label - 1, score, i]
        a = z1
        b = y1
        c = x1
        d = z2
        e = y2
        f = x2
        i = image """

    paths = []
    p1 = "Output/sliced_IS_resized"
    path_pos = [f.path for f in os.scandir(p1) if f.is_dir()]
    for x in path_pos:
        # p = x.repace("\\" ,"/")
        path_dim = [f.path for f in os.scandir(x) if f.is_dir()]
        paths = paths + path_dim

    for itr in range(len(paths)):
        path = paths[itr]
        print("Working on Visualization on path " + str(itr) + " out of " + str(len(paths)))




        with open(path + '/predictions.pickle', 'rb') as handle:
            predictions = pickle.load(handle)




        files = [f for f in listdir(path) if isfile(join(path, f))]
        files.remove('predictions.pickle')
        number_of_pred = len(predictions)
        counter = 0

        for x in range(number_of_pred):

            data = predictions[x]
            selected_image = int(data[8])
            selected_image = files[selected_image]
            working_image = path + "/" + selected_image
            im = np.array(Image.open(working_image))


            z1 = int(data[0] * 64)
            x1 = int(data[1] * 64)
            y1 = int(data[2] * 64)
            z2 = int(data[3] * 64) - 1
            x2 = int(data[4] * 64) - 1
            y2 = int(data[5] * 64) - 1
            Feature = data[6]
            prop = data[7]

            if prop >= 0.3:

                path_out = path.replace("sliced_IS_resized", "Visualized")
                if not os.path.exists(path_out):
                    os.makedirs(path_out)

                #print("found feature " + str(Feature) + " in picture " + working_image )

                # z1,y1,x1,z2,y2,x2 = reomove_rotations(z1,y1,x1,z2,y2,x2,rotations[x])

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

                color = color[0:3][::-1]
                im[x1][y1] = color
                im[x2][y2] = color

                for x in range(x2 - x1):
                    im[x1 + x][y1] = color
                    im[x1 + x][y2] = color

                for x in range(y2 - y1):
                    im[x1][y1 + x] = color
                    im[x2][y1 + x] = color

                im = Image.fromarray(im)
                im.save(path_out + "/" + selected_image.replace(".png", "_"+str(counter)+".png"))

                img = Image.open(path_out + "/" + selected_image.replace(".png", "_"+str(counter)+".png"))
                img = img.resize((1000, 1000), Image.ANTIALIAS)
                img.save(path_out + "/" + selected_image.replace(".png", "_"+str(counter)+".png"))

                counter+=1

        """            if i == 1:
                        a = 1-z2
                        b = 1-y2
                        c = x1
                        d = 1-z1
                        e = 1-y1
                        f = x2
                    elif i == 2:
                        a = y1
                        b = 1-z2
                        c = x1
                        d = y2
                        e = 1-z1
                        f = x2
                    elif i == 3:
                        a = 1-y2
                        b = z1
                        c = x1
                        d = 1-y1
                        e = z2
                        f = x2
                    elif i == 4:
                        a = 1-x2
                        b = y1
                        c = z1
                        d = 1-x1
                        e = y2
                        f = z2
                    elif i == 5:
                        a = x1
                        b = y1
                        c = 1-z2
                        d = x2
                        e = y2
                        f = 1-z1"""
