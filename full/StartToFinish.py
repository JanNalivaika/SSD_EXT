from Scripts.Slicer import Slicer
from Scripts.Bar_Remover import Remover
from Scripts.Combiner import Voxel_Combiner
from Scripts.PNGfromArray import PNG_Creator
from Scripts.Segment import Segment
from Scripts.SSD.test import *
from Scripts.Visualize import Visualize
import shutil

def deleteOLD():
    ## If folder exists, delete it ##
    remove_path = "Output"
    try:
        shutil.rmtree(remove_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == '__main__':




    file = "STL_files/ALL_TURNED.stl"
    resolution = 3000

    dim_step = 1.5
    NN_dim = 64
    overlap = 0.3

    #deleteOLD()
    #Slicer(file, resolution)
    #Remover()
    #Voxel_Combiner()
    #PNG_Creator()
    #Segment(dim_step,NN_dim,overlap)
    #Recognize()
    #Visualize()
    #TURN IS POSSIBLE !!!!
    #Reconstruct()

