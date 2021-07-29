import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob

IMG_list = glob.glob("data/*.png")
NPY_list = glob.glob("data/*.npy")

for file in range(len(IMG_list)):

    data = np.load(NPY_list[file])
    im = np.array(Image.open(IMG_list[file]))
    for element in range(len(data)):

        ymin = int(data[element][0] * 64)  # ymin
        xmin = int(data[element][1] * 64)  # xmin
        ymax = int(data[element][2] * 64) - 1  # xmax
        xmax = int(data[element][3] * 64) - 1  # ymax
        DEPTH_OF_FEATURE = data[element][4] * 64
        Feature = int(data[element][5])

        color = [255, 0, 0, 255]

        color = {
            0: [255, 255, 0, 255],
            1: [255, 0, 0, 255],
            2: [0, 255, 0, 255],
            3: [0, 0, 255, 255],
            4: [255, 127, 0, 255],
            5: [255, 212, 0, 255],
            6: [255, 255, 0, 255],
            7: [191, 255, 0, 255],
            8: [106, 255, 0, 255],
            9: [0, 234, 255, 255],
            10: [0, 149, 255, 255],
            11: [0, 64, 255, 255],
            12: [170, 0, 255, 255],
            13: [255, 0, 170, 255],
            14: [237, 185, 185, 255],
            15: [231, 233, 185, 255],
            16: [185, 237, 224, 255],
            17: [185, 215, 237, 255],
            18: [220, 185, 237, 255],
            19: [143, 35, 35, 255],
            20: [143, 106, 3, 255],
            21: [79, 143, 35, 255],
            22: [35, 98, 143, 255],
            23: [107, 35, 143, 255],
            24: [115, 115, 115, 255],
            25: [204, 204, 204, 255]
        }[Feature]

        im[xmin][ymin] = color
        im[xmax][ymax] = color

        for x in range(xmax - xmin):
            im[xmin + x][ymin] = color
            im[xmin + x][ymax] = color

        for x in range(ymax - ymin):
            im[xmin][ymin + x] = color
            im[xmax][ymin + x] = color

    new_name = IMG_list[file].replace("data\\", "")
    new_name = new_name.replace(".png", "_VF_" + str(len(data)) + ".png")
    im = Image.fromarray(im)
    im.save("augmented/augmented_" + new_name)

    basewidth = 500
    img = Image.open("augmented/augmented_" + new_name)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save("augmented/augmented_" + new_name)
