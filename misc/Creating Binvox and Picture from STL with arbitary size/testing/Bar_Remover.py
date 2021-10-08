import math
import numpy as np
from os import listdir
from os.path import isfile, join
from matplotlib.image import imread, imsave

path = "output"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

bars = []

# use thin in loop len(onlyfiles)

for file in range(3):
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
    image = image[:-remove, :, :]
    imsave(place, image)
