from voxelfuse.voxel_model import VoxelModel
from voxelfuse.mesh import Mesh
from voxelfuse.primitives import generateMaterials
import numpy as np
import time
import random
import math
import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
import binvox_rw


def SEVEasSTL(block):
    block = block.tolist()

    for x in range(size):
        for y in range(size):
            for z in range(size):
                block[x][y][z] = int(block[x][y][z])

    model = VoxelModel(block, generateMaterials(0))  # 4 is aluminium.
    mesh = Mesh.fromVoxelModel(model)
    mesh.export("NEW.stl")


def SAVEasBINVOX(block):
    newfile = open('NEW.binvox', 'wb')
    block = block.tolist()
    for x in range(64):
        for y in range(64):
           for z in range(64):
                if block[x][y][z] == 1:
                    block[x][y][z] = True
                else:
                    block[x][y][z] = False

    dims = [64, 64, 64]
    translate = 0
    scale = 10
    axis_order = 'xyz'
    m2 = binvox_rw.Voxels(block, dims, translate, scale, axis_order)
    m2.write(newfile)

def SubractFeature(xmin,ymin,xmax,ymax,block,Feature, DEPTH_OF_FEATURE):

    # take hi-rez Hexagon
    if Feature == 22:
        picture = "hexagon"

    # sclale down to width

    width = xmax - xmin
    height = ymax - ymin

    img = Image.open(picture + ".png")
    #wpercent = (width / float(img.size[0]))
    #height = int((float(img.size[1]) * float(wpercent)))

    img = img.resize((height, width))
    img.save("lowres" + picture + ".png")
    hex = np.array(img)

    # replace elements

    for depth in range(DEPTH_OF_FEATURE):
        for x in range(width):
            for y in range(height):
                if sum(hex[x][y]) != 255 * 3:
                    block[xmin + x][ymin + y][63 - depth] = 0



    return block

size = 64
block = (np.ones((size, size, size)))

IMG_list = glob.glob("Data/*.png")
NPY_list = glob.glob("Data/*.npy")

for files in range(len(IMG_list)):
    data = np.load(NPY_list[files])
    im = np.array(Image.open(IMG_list[files]))

    for element in range(len(data)):
        ymin = int(data[element][0] * 64)  # ymin
        xmin = int(data[element][1] * 64)  # xmin
        ymax = int(data[element][2] * 64) - 1  # xmax
        xmax = int(data[element][3] * 64) - 1  # ymax
        DEPTH_OF_FEATURE = int(data[element][4] * 64)+1
        Feature = int(data[element][5])

        if Feature == 22:
            block = SubractFeature(xmin,ymin,xmax,ymax,block,Feature, DEPTH_OF_FEATURE)

            SEVEasSTL(block)
            SAVEasBINVOX(block)





