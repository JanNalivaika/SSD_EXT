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


    t1= time.time()

    file = "STL_files/ALL_TURNED.stl"
    resolution = 3000
    # 3000 new = 3.1 h
    # 3000 old = 6.0 min

    dim_step = 1.2
    NN_dim = 64
    overlap = 1/3

    deleteOLD()
    Slicer(file, resolution)

    Remover()           # may be obsolete
    Voxel_Combiner()    # may be obsolete
    PNG_Creator()       # may be obsolete

    #PNG_Creator_from_BOOL()

    Segment(dim_step,NN_dim,overlap)
    Recognize()
    Visualize()
    #TURN IS POSSIBLE !!!!
    #Reconstruct()

    print(time.time()-t1)

