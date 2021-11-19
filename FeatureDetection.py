from Scripts.Slicer import Slicer
from Scripts.Segment import Segment
from Scripts.SSD.test import *
from Scripts.Visualize import Visualize
from Scripts.STLturner import turnSTL
from Scripts.PNGfromArrayBOOL import PNG_Creator_from_BOOL
from Scripts.Reconstruction import Reconstruct
from Scripts.Resolution import Set_Resolution
import shutil
import time
import math


def deleteOLD():
    ## If folder exists, delete it ##
    ## For a clean start every time ##
    remove_path = "Output"
    try:
        shutil.rmtree(remove_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


if __name__ == '__main__':
    t = time.time()  # Starting time to time everything
    speed = 1  # speed variable: Impacts resolution, dimension, step_size, overlap,
    file = "STL_Files/paper.stl"  # SELECT STL-FILES HERE
    resolution, dim_start = Set_Resolution(file)
    resolution = max(int(resolution / speed), 64) # Resolution has to be at least 64
    # !!!ATTENTION!!! low resolution == High detail! a lil bit counterintuitive
    dim_start = int(dim_start * speed)  # can be impacted by speed variable
    print("NOT WORKING ON CUBES!!!!")  # this is a problem
    print("NOT WORKING ON CUBES!!!!")  # this is a problem
    print("NOT WORKING ON CUBES!!!!")  # this is a problem

    dim_step = int(resolution / 20 * speed)  # Equivalent to step_size; in proportion to speed
    NN_dim = 64  # setting NN Dimension
    overlap = 2 / 4 / speed   # setting overlap

    deleteOLD()  # deleting files from previous runs
    t1 = time.time()
    turnSTL(file)  # Turning the STL file to face axis
    print("Turning  Time: " + str(time.time() - t1))

    t1 = time.time()  # timing Slicer
    Slicer(resolution)  # ERRORS ARISE HERE !!!!!! NOT WORKING ON CUBES
    print("Slicer Time: " + str(time.time() - t1))

    png_precision = int(math.ceil(speed))*2-1  # setting PNG precision; impacts execution speed significantly
    t1 = time.time()  # timing PNG creator
    PNG_Creator_from_BOOL(png_precision)  # fixed loop in loop
    print("PNG creator time Time " + str(time.time() - t1))

    t1 = time.time()  # timing PNG Segmentation
    Segment(dim_start, dim_step, NN_dim, overlap)
    print("Segmentation Time: " + str(time.time() - t1))

    t1 = time.time()  # timing Recognition
    Recognize()  # Running recognition 99% of time is spend here
    print("Recognition Time: " + str(time.time() - t1))

    t1 = time.time()  # timing Visualization
    #Visualize()
    #print("Visualize Time: " + str(time.time() - t1))

    t1 = time.time()  # timing Reconstruction
    Reconstruct(0.99)
    print("Reconstruct Time: " + str(time.time() - t1))

    print("OVERALL Time: " + str(time.time() - t))

    """
    CPU 
    Turning  Time: 0.13962793350219727
    Slicer Time: 20.721684455871582
    PNG creator time Time 15.659171342849731
    Segmentation Time: 33.39087700843811
    Recognition Time: 85.50972890853882
    Reconstruct Time: 0.510636568069458
    OVERALL Time: 157.3928234577179
    
    
    GPU
    Turning  Time: 0.08477282524108887
    Slicer Time: 22.21677875518799
    PNG creator time Time 16.4051513671875
    Segmentation Time: 33.71016716957092
    Recognition Time: 41.68975520133972
    Reconstruct Time: 0.42287182807922363
    OVERALL Time: 116.05442452430725
    
    """
