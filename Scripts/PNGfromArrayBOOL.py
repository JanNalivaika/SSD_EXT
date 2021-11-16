import time

import numpy as np
from PIL import Image
import pickle
import os
import numpy as np
import os
from os import listdir
from os.path import isfile, join

def PNG_Creator_from_BOOL(png_precision):

    def XRay(block, file, png_precision, rot):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, w, 3), dtype=np.uint8)
        #, dtype=np.uint8
        inc = (255 / d)
        #print(l)
        for x in range(l):
            #print(x)
            for y in range(w):
                new_color = 0
                for z in range(0, d, png_precision):
                    if int(block[x][y][z]) != 1:
                        new_color += inc
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color


        #data = np.array(data).astype(int)
        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_xray_rotation_" +str(rot) +".png"
        img.save(filename)
        # img.show()


    def MakeAPicture_1_2(block, file, png_precision, rot):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        dataF = np.zeros((l, w, 3), dtype=np.uint8)
        dataB = np.zeros((l, w, 3), dtype=np.uint8)
        inc = 255 / d

        for x in range(0, (l), 1):
            for y in range(0, (w), 1):
                new_color = 0
                """
                for z in range(0, (d), png_precision):


                    if block[x][y][z]:
                        break
                    else:
                        new_color += inc * png_precision

                """

                test = block[x,y,:]
                test = np.where(test == True)

                try:
                    front = test[0][0]
                    back = d - test[-1][-1]
                except:
                    front = d
                    back = d

                new_colorF = inc * front


                if new_color > 255:
                    new_color = 255
                dataF[x][y][0] = new_colorF
                dataF[x][y][1] = new_colorF
                dataF[x][y][2] = new_colorF

                new_colorB = inc * back

                if new_color > 255:
                    new_color = 255
                dataB[x][y][0] = new_colorB
                dataB[x][y][1] = new_colorB
                dataB[x][y][2] = new_colorB

        img = Image.fromarray(dataB, 'RGB')
        filename = file + "\HD_top_rotation_" + str(rot) + ".png"
        img.save(filename)
        # img.show()

        img = Image.fromarray(dataF, 'RGB')
        filename = file + "\HD_bottom_rotation_" +str(rot) +".png"
        img.save(filename)
        # img.show()


    def MakeAPicture2(block, file, png_precision,rot):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, w, 3), dtype=np.uint8)
        inc = 255 / d

        for x in range(0, (l), 1):
            for y in range(0, (w), 1):
                new_color = 0
                """for z in range(0, (d), png_precision):
                    if (block[x][y][d - 1 - z]):
                        break
                    else:
                        new_color += inc * png_precision"""

                test = block[x, y, :]
                test = np.where(test == True)
                test = d-test[-1][-1]
                new_color = inc * test

                if new_color > 255:
                    new_color = 255
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_top_rotation_" +str(rot) +".png"
        img.save(filename)
        # img.show()


    def MakeAPicture_3_4(block, file, png_precision,rot):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        dataF = np.zeros((w, d, 3), dtype=np.uint8)
        dataB = np.zeros((w, d, 3), dtype=np.uint8)
        inc = 255 / l

        for x in range(0, (w), 1):
            for y in range(0, (d), 1):
                new_color = 0
                """for z in range(0, (l), png_precision):

                    if block[z][x][y]:
                        break
                    else:
                        new_color += inc * png_precision"""

                test = block[:, x, y]
                test = np.where(test == True)

                try:
                    front = test[0][0]
                    back = l - test[-1][-1]
                except:
                    front = l
                    back = l

                new_colorF = inc * front

                if new_color > 255:
                    new_color = 255
                dataF[x][y][0] = new_colorF
                dataF[x][y][1] = new_colorF
                dataF[x][y][2] = new_colorF

                new_colorB = inc * back

                if new_colorB > 255:
                    new_colorB = 255
                dataB[x][y][0] = new_colorB
                dataB[x][y][1] = new_colorB
                dataB[x][y][2] = new_colorB

        if rot == 0:
            img = Image.fromarray(dataF, 'RGB')
            filename = file + "\HD_left_rotation_" +str(rot) +".png"
            img.save(filename)
            # img.show()

        img = Image.fromarray(dataB, 'RGB')
        filename = file + "\HD_right_rotation_" + str(rot) + ".png"
        img.save(filename)


    def MakeAPicture4(block, file, png_precision,rot):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((w, d, 3), dtype=np.uint8)
        inc = 255 / l

        for x in range(0, (w), 1):
            for y in range(0, (d), 1):
                new_color = 0
                for z in range(0, (l), png_precision):
                    if block[l - 1 - z][x][y]:
                        break
                    else:
                        new_color += inc * png_precision

                if new_color > 255:
                    new_color = 255
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_right_rotation_" +str(rot) +".png"
        img.save(filename)
        # img.show()


    def MakeAPicture_5_6(block, file, png_precision,rot):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        dataF = np.zeros((l, d, 3), dtype=np.uint8)
        dataB = np.zeros((l, d, 3), dtype=np.uint8)
        inc = 255 / w

        for x in range(0, (l), 1):
            for y in range(0, (d), 1):
                new_color = 0



                """for z in range(0, (w), png_precision):
                    if block[x][z][y]:
                        break
                    else:
                        new_color += inc * png_precision"""

                test = block[x, :, y]
                test = np.where(test == True)
                try:
                    front = test[0][0]
                    back = w - test[-1][-1]
                except:
                    front = w
                    back = w


                new_colorF = inc * front

                if new_color > 255:
                    new_color = 255
                dataF[x][y][0] = new_colorF
                dataF[x][y][1] = new_colorF
                dataF[x][y][2] = new_colorF

                new_colorB = inc * back


                if new_colorB > 255:
                    new_colorB = 255
                dataB[x][y][0] = new_colorB
                dataB[x][y][1] = new_colorB
                dataB[x][y][2] = new_colorB

        img = Image.fromarray(dataF, 'RGB')
        filename = file + "\HD_front_rotation_" +str(rot) +".png"
        img.save(filename)
        #img.show()

        img = Image.fromarray(dataB, 'RGB')
        filename = file + "\HD_back_rotation_" +str(rot) +".png"
        img.save(filename)
        #img.show()



    def MakeAPicture6(block, file, png_precision,rot):
        l, w, d = len(block), len(block[0]), len(block[0][0])
        data = np.zeros((l, d, 3), dtype=np.uint8)
        inc = 255 / w

        for x in range(0, (l), 1):
            for y in range(0, (d), 1):
                new_color = 0
                for z in range(0, (w), png_precision):
                    if block[x][w-1-z][y]:
                        break
                    else:
                        new_color += inc * png_precision

                if new_color > 255:
                    new_color = 255
                data[x][y][0] = new_color
                data[x][y][1] = new_color
                data[x][y][2] = new_color

        img = Image.fromarray(data, 'RGB')
        filename = file + "\HD_back_rotation_" +str(rot) +".png"
        img.save(filename)
        #img.show()




    path = 'Output/Combined_Voxel'
    STLfiles = [f for f in listdir(path) if f.endswith('.pickle')]

    for rot in range(len(STLfiles)):
        file = "Output/Combined_Voxel/" + STLfiles[rot]

        with open(file, 'rb') as handle:
            block = pickle.load(handle)

        output_path = r'Output/HD_pictures'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        block =np.asarray(block)


        #t1 = time.time()
        #print("Working on Picture 0" )
        #XRay(block, output_path, png_precision, rot)
        #print(time.time()-t1)

        # takes around 400 sec per picture

        if rot>0:
            t1 = time.time()
            #print("Working on Picture 4")
            MakeAPicture_3_4(block, output_path, png_precision, rot)  # right
            #print(time.time() - t1)
        else:
            t1 = time.time()
            #print("Working on Picture 1 + 2")
            MakeAPicture_1_2(block, output_path, png_precision, rot)  # under side
            #print(time.time() - t1)
            #t1 = time.time()
            #print("Working on Picture 2")
            #MakeAPicture2(block, output_path, png_precision, rot)  # top side
            #print(time.time() - t1)
            t1 = time.time()
            #print("Working on Picture 3 + 4")
            MakeAPicture_3_4(block, output_path, png_precision, rot)  # left
            #print(time.time() - t1)
            t1 = time.time()
            #print("Working on Picture 4")
            #MakeAPicture4(block, output_path, png_precision, rot)  # right
            #print(time.time() - t1)
            t1 = time.time()
            #print("Working on Picture 5 + 6")
            MakeAPicture_5_6(block, output_path, png_precision, rot)
            #print(time.time() - t1)
            #t1 = time.time()
            #print("Working on Picture 6")
            #MakeAPicture6(block, output_path, png_precision, rot)
            #print(time.time() - t1)
