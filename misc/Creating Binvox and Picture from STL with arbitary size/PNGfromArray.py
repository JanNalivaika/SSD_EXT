import numpy as np
from PIL import Image
import pickle


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
    filename = file.replace(".pickle", "_xray.png")
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
    filename = file.replace(".pickle", "_bottom.png")
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
    filename = file.replace(".pickle", "_top.png")
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
    filename = file.replace(".pickle", "_left.png")
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
    filename = file.replace(".pickle", "_right.png")
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
    filename = file.replace(".pickle", "_front.png")
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
    filename = file.replace(".pickle", "_back.png")
    img.save(filename)
    #img.show()


if __name__ == '__main__':
    file = 'new.pickle'
    with open(file, 'rb') as handle:
        block = pickle.load(handle)
    XRay(block, file)
    MakeAPicture1(block, file)  # under side
    MakeAPicture2(block, file)  # top side
    MakeAPicture3(block, file)  # left
    MakeAPicture4(block, file)  # right
    MakeAPicture5(block, file)
    MakeAPicture6(block, file)
