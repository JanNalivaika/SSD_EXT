import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join
import os


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

    dim = len(np.array(Image.open(mypath + element)))

    picture_x += dim
    picture_y += dim

    Restored = np.asarray([[[0, 0, 0] for x in range(picture_y)] for y in range(picture_x)])

    for element in files:
        data = np.array(Image.open(mypath + element))
        name = element.replace(".png", "").split("_")
        xpos = int(name[0])
        ypos = int(name[1])

        # what si goung on here ????????????????????????????
        # slicing assigment did not work ???????????????
        for x in range(dim):
            for y in range(dim):
                Restored[x + xpos][y + ypos] = data[x][y][0:3]

    img = Image.fromarray(Restored.astype(np.uint8), "RGB")

    img.save("REconstructed/REconstructed.png")

    return 0


def Segment(file, dim_step, overlap, NN_dim, dim):
    picture = np.asarray(Image.open(file))

    max_x_dim = len(picture)
    max_y_dim = len(picture[0])

    if max_x_dim > max_y_dim:
        picture = np.transpose(picture, (1, 0, 2))

    max_x_dim = len(picture)
    max_y_dim = len(picture[0])
    xpos = 0
    ypos = 0
    now_Special = False
    stopper = 0

    while dim <= max_x_dim and dim <= max_y_dim:

        newpath = "pictures_NON_resized/" + str(dim)
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        while (ypos <= max_y_dim - dim):
            xpos = 0
            while (xpos <= max_x_dim - dim):
                segment = picture[xpos:xpos + dim, ypos:ypos + dim]
                img = Image.fromarray(segment, 'RGB')
                img.save(newpath + "/" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')
                xpos += int(dim * (1-overlap))
            # hanging picture at the end
            segment = picture[max_x_dim - dim:max_x_dim, ypos:ypos + dim]
            img = Image.fromarray(segment, 'RGB')
            xpos = max_x_dim - dim
            img.save(newpath + "/" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')
            ypos += int(dim * (1-overlap))

        # loop for hanging pictures at the side

        xpos = 0
        while (xpos <= max_x_dim - dim):
            segment = picture[xpos:xpos + dim, max_y_dim - dim:max_y_dim]
            ypos = max_y_dim - dim
            img = Image.fromarray(segment, 'RGB')
            img.save(newpath + "/" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')
            xpos += int(dim * (1-overlap))

        # hanging picture at the end on the side
        segment = picture[max_x_dim - dim:max_x_dim, max_y_dim - dim:max_y_dim]
        img = Image.fromarray(segment, 'RGB')
        xpos = max_x_dim - dim
        ypos = max_y_dim - dim
        img.save(newpath + "/" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')
        xpos += int(dim * (1-overlap))

        if now_Special is True:
            if int(stopper) is 1:
                break
                break
            leftover = max(max_y_dim, max_x_dim) - min(max_y_dim, max_x_dim)
            to_append = np.asarray([[[255, 255, 255] for x in range(max_y_dim)] for y in range(leftover)])
            picture = np.append(picture, to_append, axis=0)
            picture = picture.astype(np.uint8)
            max_y_dim = len(picture)
            max_x_dim = len(picture)
            now_Special = False

        dim = int(dim_step * dim)

        if dim > max_x_dim or dim > max_y_dim:
            dim = min(max_y_dim, max_x_dim)
            now_Special = True
            stopper += 0.5

        xpos = 0
        ypos = 0

    # this is the special part

    # do_special_images(file, max_y_dim, max_x_dim)

    # this is the RESIZING
    place = [x[0] for x in os.walk("pictures_NON_resized/")]
    for old_folder in place:
        new_folder = old_folder.replace("NON", "IS")
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        files = [f for f in listdir(old_folder) if isfile(join(old_folder, f))]

        for file in files:
            img = Image.open(old_folder + "/" + file)
            img = img.resize((NN_dim, NN_dim))
            if np.sum(np.asarray(img)) != 255*3*64*64:
                img.save(new_folder + "/" + file)


def do_special_images(file, max_y_dim, max_x_dim):
    newpath = "pictures_NON_resized/special"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    picture = np.asarray(Image.open(file))
    square = max(max_y_dim, max_x_dim)
    leftover = max(max_y_dim, max_x_dim) - min(max_y_dim, max_x_dim)
    if max_y_dim > max_x_dim:
        to_append = np.asarray([[[255, 255, 255] for x in range(max_y_dim)] for y in range(leftover)])
        picture = np.append(picture, to_append, axis=0)
        img = Image.fromarray(picture.astype(np.uint8), 'RGB')
        img.save(newpath + "/" + 'total.png')


if __name__ == "__main__":
    file = "BIG.png"
    dim_step = 2
    NN_dim = 64
    dim = 64
    overlap = 0.1
    Segment(file, dim_step, overlap, NN_dim, dim)
    # Construct()
