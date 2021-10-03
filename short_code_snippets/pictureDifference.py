from PIL import Image
import numpy as np

im1 = np.array(Image.open("1.png"))
im2 = np.array(Image.open("2.png"))

for x in range(im1.shape[0]):
    for y in range(im1.shape[1]):
        for z in range(im1.shape[2]):
            if int(im1[x][y][z]) != int(im2[x][y][z]):
                a = int(im1[x][y][z])
                b = int(im2[x][y][z])
                im1[x][y][z] = a-b

a = im1.__sub__(im2)
im = Image.fromarray(a)
im.save("erg.png")
