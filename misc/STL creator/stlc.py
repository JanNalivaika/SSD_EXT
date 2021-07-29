from voxelfuse.voxel_model import VoxelModel
from voxelfuse.mesh import Mesh
from voxelfuse.primitives import generateMaterials
import numpy as np
import time
import random
import math


base = []

for iter in range(1000):
    size = 80
    block = (np.ones((size, size, size)))
    t1 = time.time()
    while True:
        depthMAX = math.floor((size * 0.9))
        depthMIN = math.floor((size / 10))
        depth = random.randint(depthMIN, depthMAX)

        pMAX = math.floor((size * 0.3))
        p = random.randint(3, pMAX)  # muss ungerade sein
        if p % 2 == 0:
            p += 1

        wMAX = math.floor((size * 0.5))
        w = random.randint(p + 2, wMAX)  # muss ungerade sein
        if w % 2 == 0:
            w += 1

        lMAX = math.floor((size * 0.3))
        lMIN = math.floor((size * 0.1))
        l = random.randint(lMIN, lMAX)

        posx = random.randint(0 + (w - 1) / 2, (size - (w - 1) / 2)-1)

        tMAX = math.floor((size * 0.3))
        tMIN = math.floor((size * 0.1))
        t = random.randint(tMIN, tMAX)

        posy = random.randint(t, size - l - 1)

        if [depth,p,w,l,t,posx,posy] not in base:
            break

    base.append([depth,p,w,l,t,posx,posy])

    for x in range(size):  # depth from back to front
        for y in range(size):  # from bottom to top
            for z in range(size):  # cutting depth
                if z >= size - depth:
                    if x == posx and y == posy:
                        block[x][y][z] = 0
                    if posx - (p - 1) / 2 <= x <= posx + (p - 1) / 2 and posy + l >= y > posy:  # topslot
                        block[x][y][z] = 0

                    if posx + (w - 1) / 2 >= x >= posx - (w - 1) / 2 and posy - t < y <= posy:  # sideslot
                        block[x][y][z] = 0



    change = random.randint(0,3)
    a = (np.ones((size, size, size)))
    b = (np.ones((size, size, size)))
    c = (np.ones((size, size, size)))
    if change == 1:  # turn left
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    a[size-1-y][x][z] = block[x][y][z]
        block=a

    if change == 2:  # turn left left
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    a[size-1-y][x][z] = block[x][y][z]
        for x in range(size):
            for y in range(size):
                for z in range(size):
                     b[size - 1 - y][x][z] = a[x][y][z]
        block=b

    if change == 3:  # turn left left left
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    a[size-1-y][x][z] = block[x][y][z]
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                       b[size - 1 - y][x][z] = a[x][y][z]
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                        c[size - 1 - y][x][z] = b[x][y][z]
        block = c

    block = block.tolist()

    for x in range(size):
        for y in range(size):
            for z in range(size):
                block[x][y][z] = int(block[x][y][z])

    model = VoxelModel(block, generateMaterials(0))  # 4 is aluminium.
    mesh = Mesh.fromVoxelModel(model)
    mesh.export("25_"+str(iter)+".stl")
    t2 = time.time()
    print(t2 - t1)



