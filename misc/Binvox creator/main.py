import binvox_rw
import numpy as np
import random
import math
import time


def getBLOCK():
    size = 64
    block = (np.ones((size, size, size)))
    t1 = time.time()

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

    posx = random.randint(0 + (w - 1) / 2, (size - (w - 1) / 2) - 1)

    tMAX = math.floor((size * 0.3))
    tMIN = math.floor((size * 0.1))
    t = random.randint(tMIN, tMAX)

    posy = random.randint(t, size - l - 1)


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


    block = block.tolist()

    for x in range(size):
        for y in range(size):
            for z in range(size):
                block[x][y][z] = int(block[x][y][z])

    for x in range(size):
        for y in range(size):
           for z in range(size):
                if block[x][y][z] == 1:
                    block[x][y][z] = True
                else:
                    block[x][y][z] = False

    return block


original = open('0_3.binvox', 'br')
lol = original.read()
# x01\xff true?




newfile = open('000.binvox', 'wb')


size = 64
block = getBLOCK()


dims = [64, 64, 64]
translate = 0
scale = 10
axis_order = 'xyz'
m2 = binvox_rw.Voxels(block, dims, translate, scale, axis_order)
m2.write(newfile)
