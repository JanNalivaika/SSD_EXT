
from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
import pickle
from natsort import natsorted
import os


path = "output"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
onlyfiles = natsorted(onlyfiles)

# for getting dims
img = Image.open(path + "/" + onlyfiles[0])
img = np.array(img)
dim1 = len(img)
dim2 = len(img[0])
dim3 = len(onlyfiles)

block = np.zeros((dim1, dim2, dim3), dtype=np.uint8)
combined = np.asarray([])
arr = [255,255,255,255]

for file in range(dim3):
    print("combing file " + str(file) + " out of " + str(dim3))
    img = Image.open(path + "/" + onlyfiles[file])
    img = np.array(img)
    for x in range(dim1):
        for y in range(dim2):
            slit = img[x][y]
            if np.array_equiv(arr, slit):
                block[x][y][file] = 1



with open("../new.pickle", 'wb') as handle:
    pickle.dump(block, handle, protocol=pickle.HIGHEST_PROTOCOL)
