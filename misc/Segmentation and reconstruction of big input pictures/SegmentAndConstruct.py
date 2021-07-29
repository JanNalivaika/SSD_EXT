import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join


def Segment(file, overlap, dimension):
    picture = np.asarray(Image.open(file))
    max_x_dim = len(picture)
    max_y_dim = len(picture[0])
    xpos = 0
    ypos = 0

    while (ypos < max_y_dim - dimension):
        xpos = 0
        while (xpos < max_x_dim - dimension):
            segment = picture[xpos:xpos + dimension, ypos:ypos + dimension]
            img = Image.fromarray(segment, 'RGB')
            img.save("Segmented/" + str(xpos) + "_" + str(ypos) + '.png')
            xpos += overlap
        #hanging picture at the end
        segment = picture[max_x_dim-dimension:max_x_dim , ypos:ypos + dimension]
        img = Image.fromarray(segment, 'RGB')
        xpos = max_x_dim-dimension
        img.save("Segmented/" + str(xpos) + "_" + str(ypos) + '.png')
        ypos += overlap

    # loop for hanging pictures at the side


    xpos = 0
    while (xpos < max_x_dim - dimension):
        segment = picture[xpos:xpos + dimension, max_y_dim-dimension:max_y_dim]
        ypos = max_y_dim - dimension
        img = Image.fromarray(segment, 'RGB')
        img.save("Segmented/" + str(xpos) + "_" + str(ypos) + '.png')
        xpos += overlap

    # hanging picture at the end on the side
    segment = picture[max_x_dim - dimension:max_x_dim, max_y_dim - dimension:max_y_dim]
    img = Image.fromarray(segment, 'RGB')
    xpos = max_x_dim - dimension
    ypos = max_y_dim - dimension
    img.save("Segmented/" + str(xpos) + "_" + str(ypos) + '.png')
    xpos += overlap

def Construct():
    mypath = "Segmented/"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    picture_x = 0
    picture_y = 0
    for element in files:
        name = element.replace(".png", "").split("_")
        xpos = int(name[0])
        ypos = int(name[1])

        if xpos > picture_x:
            picture_x = xpos
        if ypos > picture_y:
            picture_y = ypos
    dimension = len(np.array(Image.open(mypath + element)))

    picture_x +=dimension
    picture_y += dimension

    Restored = np.asarray([[[0,0,0] for x in range(picture_y)] for y in range(picture_x)])

    for element in files:
        data = np.array(Image.open(mypath + element))
        name = element.replace(".png", "").split("_")
        xpos = int(name[0])
        ypos = int(name[1])

        # what si goung on here ????????????????????????????
        # slicing assigment did not work ???????????????
        for x in range(dimension):
            for y in range(dimension):
                Restored[x+xpos][y+ypos] = data[x][y][0:3]


    img = Image.fromarray(Restored.astype(np.uint8),"RGB")

    img.save("REconstructed/REconstructed.png")

    return 0



file = "BIG.png"
Step = 10  # in pixel
dimension = 64

Segment(file, Step, dimension)
Construct()

