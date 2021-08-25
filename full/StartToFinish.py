from Scripts.Slicer import Slicer
from Scripts.Bar_Remover import Remover
from Scripts.Combiner import Voxel_Combiner
from Scripts.PNGfromArray import PNG_Creator
from Scripts.Segment import Segment
from Scripts.SSD.test import *
from Scripts.Visualize import Visualize
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

    file = "STL_files/StartToFinish.stl"
    resolution = 3000
    # 3000 new optimized  = 40 min
    # 3000 new = 3.1 h
    # 3000 old = 6.0 min

    dim_step = 1.5
    NN_dim = 64
    overlap = 1/3

    deleteOLD()
    Slicer(file, resolution)

    #Remover()           # IS obsolete
    #Voxel_Combiner()    # IS be obsolete
    #PNG_Creator()       # IS be obsolete

    PNG_Creator_from_BOOL()

    Segment(dim_step,NN_dim,overlap)
    Recognize()
    Visualize()
    #TURN IS POSSIBLE !!!!
    # To Do : IMPLEMENT TURNING HERE !

    #Reconstruct()

    print(time.time()-t)

