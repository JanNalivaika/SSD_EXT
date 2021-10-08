from Scripts.Slicer import Slicer
from Scripts.Bar_Remover import Remover
from Scripts.Combiner import Voxel_Combiner
from Scripts.PNGfromArray import PNG_Creator
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
    remove_path = "Output"
    try:
        shutil.rmtree(remove_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == '__main__':

    t = time.time()
    speed = 1
    file = "STL_files/allinone.stl"
    resolution = int(Set_Resolution(file)/speed)
    print(resolution)
    print("NOT WORKING ON CUBES")


    dim_step = int(resolution/25*speed) # ???????????????????????????????
    dim_start = int(resolution/10)
    dim_start = 64# ???????????????????????????????
    NN_dim = 64 # ???????????????????????????????
    overlap = 2/3/speed # ???????????????????????????????

    deleteOLD()

    turnSTL(file)

    t1 = time.time()
    Slicer(resolution)  # worst case 420 sec
    print("Slicer Time: " + str(time.time()-t1))
    #Remover()           # IS obsolete
    #Voxel_Combiner()    # IS be obsolete
    #PNG_Creator()       # IS be obsolete

    png_precision = int(math.ceil(speed))
    t1 = time.time()
    PNG_Creator_from_BOOL(png_precision)  # worst case __sec
    print("PNG creator time Time " + str(time.time()-t1))

    t1 = time.time()
    Segment(dim_start,dim_step,NN_dim,overlap)
    print("Segmentation Time: " + str(time.time()-t1))



    t1 = time.time()
    Recognize()
    print("Recognition Time: " + str(time.time()-t1))

    t1 = time.time()
    Visualize()
    print("Visualize Time: " + str(time.time()-t1))

    t1 = time.time()
    Reconstruct()
    print("Reconstruct Time: " + str(time.time() - t1))

    print("OVERALL Time: " + str(time.time() - t))

