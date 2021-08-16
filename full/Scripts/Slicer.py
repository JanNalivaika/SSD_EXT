from Scripts.stltovoxel import *
import numpy as np
import os


def Slicer(file,resolution):
    array = np.zeros((resolution, resolution, resolution), dtype=np.uint8)
    del array

    output_path= r'Output/Sliced'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    convert_file(file, output_path + '/HD', resolution)
