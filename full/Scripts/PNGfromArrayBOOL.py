import time

import numpy as np
from PIL import Image
import pickle
import os
import numpy as np

def PNG_Creator_from_BOOL():

    def XRay(block, file):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, w, 3), dtype=np.uint8)
        #, dtype=np.uint8
        inc = (255 / d)
        #print(l)
        for x in range(l):
            #print(x)
            for y in range(w):
                new_color = 0
                for z in range(d):
                    if int(block[x][y][z]) != 1:
                        new_color += inc
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color


        #data = np.array(data).astype(int)
        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_xray.png"
        img.save(filename)
        # img.show()


    def MakeAPicture1(block, file):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, w, 3), dtype=np.uint8)
        inc = 255 / d

        for x in range(l):
            for y in range(w):
                new_color = 0
                for z in range(d):
                    if int(block[x][y][z]) == 0:
                        new_color += inc
                    else:
                        break
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_bottom2.png"
        img.save(filename)
        # img.show()


    def MakeAPicture2(block, file):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, w, 3), dtype=np.uint8)
        inc = 255 / d

        for x in range(l):
            for y in range(w):
                new_color = 0
                for z in range(d):
                    if int(block[x][y][d - 1 - z]) == 0:
                        new_color += inc
                    else:
                        break
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_top2.png"
        img.save(filename)
        # img.show()


    def MakeAPicture3(block, file):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((w, d, 3), dtype=np.uint8)
        inc = 255 / l

        for x in range(w):
            for y in range(d):
                new_color = 0
                for z in range(l):
                    if int(block[z][x][y]) == 0:
                        new_color += inc
                    else:
                        break
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_left2.png"
        img.save(filename)
        # img.show()


    def MakeAPicture4(block, file):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((w, d, 3), dtype=np.uint8)
        inc = 255 / l

        for x in range(w):
            for y in range(d):
                new_color = 0
                for z in range(l):
                    if int(block[l - 1 - z][x][y]) == 0:
                        new_color += inc
                    else:
                        break
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_right2.png"
        img.save(filename)
        # img.show()


    def MakeAPicture5(block, file):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, d, 3), dtype=np.uint8)
        inc = 255 / w

        for x in range(l):
            for y in range(d):
                new_color = 0
                for z in range(w):
                    if int(block[x][z][y]) == 0:
                        new_color += inc
                    else:
                        break
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_front2.png"
        img.save(filename)
        #img.show()


    def MakeAPicture6(block, file):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, d, 3), dtype=np.uint8)
        inc = 255 / w

        for x in range(l):
            for y in range(d):
                new_color = 0
                for z in range(w):
                    if int(block[x][w-1-z][y]) == 0:
                        new_color += inc
                    else:
                        break
                    data[x][y][0] = new_color
                    data[x][y][1] = new_color
                    data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_back2.png"
        img.save(filename)
        #img.show()


    file = "Output/Combined_Voxel/VoxelizedSTL_BOOL.pickle"
    with open(file, 'rb') as handle:
        block = pickle.load(handle)

    output_path = r'Output/HD_pictures'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    block =np.asarray(block)


    #t1 = time.time()
    #print("Working on Picture 0" )
    #XRay(block, output_path)
    #print(time.time()-t1)

    # takes around 400 sec per picture

    t1 = time.time()
    print("Working on Picture 1")
    MakeAPicture1(block, output_path)  # under side
    print(time.time() - t1)
    t1 = time.time()
    print("Working on Picture 2")
    MakeAPicture2(block, output_path)  # top side
    print(time.time() - t1)
    t1 = time.time()
    print("Working on Picture 3")
    MakeAPicture3(block, output_path)  # left
    print(time.time() - t1)
    t1 = time.time()
    print("Working on Picture 4")
    MakeAPicture4(block, output_path)  # right
    print(time.time() - t1)
    t1 = time.time()
    print("Working on Picture 5")
    MakeAPicture5(block, output_path)
    print(time.time() - t1)
    t1 = time.time()
    print("Working on Picture 6")
    MakeAPicture6(block, output_path)
    print(time.time() - t1)
