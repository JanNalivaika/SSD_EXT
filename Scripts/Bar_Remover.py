import math
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from matplotlib.image import imread, imsave

def Remover():
    output_path = r'Output/Sliced_No_Bars'
    if not os.path.exists(output_path):
        os.makedirs(output_path)


    path = "Output\Sliced"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    bars = []

    # use thin in loop len(onlyfiles)

    for file in range(len(onlyfiles)):
        image = imread(path + "/" + onlyfiles[file])
        bar = 0
        arr = np.asarray([[0, 0, 0, 1] for y in range(len(image[1]))])
        print("checking file " + str(file) + " out of " + str(len(onlyfiles)) + " for added bar")
        for x in range(len(image)):

            arr1 = image[- 1 - x]
            if np.array_equiv(arr, arr1):
                bar += 1
            else:
                break

        print(bar)
        bars.append(bar)

    remove = min(bars)
    print(remove)

    for file in range(len(onlyfiles)):
        print("Removing bar from file " + str(file) + " out of " + str(len(onlyfiles)))
        place = path + "/" + onlyfiles[file]
        image = imread(place)
        if remove > 0:
            image = image[:-remove, :, :]
        place = output_path+ "/" + onlyfiles[file]
        imsave(place, image)
