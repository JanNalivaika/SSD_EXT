from Scripts.Slicer import Slicer
from Scripts.Bar_Remover import Remover
from Scripts.Combiner import Voxel_Combiner
from Scripts.PNGfromArray import PNG_Creator
from Scripts.Segment import Segment
from Scripts.SSD.test import *
from Scripts.Visualize import Visualize
from Scripts.STLturner import turnSTL
from Scripts.PNGfromArrayBOOL import PNG_Creator_from_BOOL
import shutil
import time


def deleteOLD():
    ## If folder exists, delete it ##
    remove_path = "Output"
    try:
        shutil.rmtree(remove_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == '__main__':


    t = time.time()

    file = "STL_files/ALL_TURNED.stl"
    resolution = 1000
    print("Why 500 not working")
    print("NOW WORKING ON CUBES")
    # 3000 png loop in step 50 = 13min
    # 3000 png loop in step 30 = 13min
    # 3000 png loop in step 20 = 14min
    # 3000 png loop in step 10 = 18min
    # 3000 png loop in step  5 = 20 min
    # 3000 png loop in step  1, 1.5, 1/3 === __ min

    dim_step = 1.5
    NN_dim = 64
    overlap = 2/3

    deleteOLD()

    turnSTL(file)

    t1 = time.time()
    Slicer(resolution)  # worst case 420 sec
    print("Slicer Time")
    print(time.time()-t1)
    #Remover()           # IS obsolete
    #Voxel_Combiner()    # IS be obsolete
    #PNG_Creator()       # IS be obsolete

    png_precision = 1
    t1 = time.time()
    PNG_Creator_from_BOOL(png_precision)  # worst case __sec
    print("PNG creator time Time")
    print(time.time() - t1)

    t1 = time.time()
    Segment(dim_step,NN_dim,overlap)
    print("Segmentation Time")
    print(time.time() - t1)


    t1 = time.time()
    Recognize()
    print("Recognition Time")
    print(time.time() - t1)


    t1 = time.time()
    Visualize()
    print("Visualize Time")
    print(time.time() - t1)


    #Reconstruct()

    print(time.time()-t)

