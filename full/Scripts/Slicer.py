from Scripts.stltovoxel import *
import numpy as np
import os
from os import listdir
from os.path import isfile, join


def Slicer(resolution):
    #array = np.zeros((resolution, resolution, resolution), dtype=np.uint8)
    #del array

    path = 'Output/STLs'
    STLfiles = [f for f in listdir(path) if (f.endswith('.stl') or f.endswith('.STL'))]


    for x in range(len(STLfiles)):
        output_path = 'Output/Sliced/' + str(x)
        file = 'Output/STLs/' + STLfiles[x]
        Fname = STLfiles[x].replace('.stl',"")
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        convert_file(file, output_path + '/HD', resolution, Fname)
