import time

import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join
import os
import cv2


"""def Construct():
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

    return 0"""


def Segment(dim_start,dim_step,NN_dim,overlap): # 3926

    path = "Output\HD_pictures"
    pictures = [f for f in listdir(path) if isfile(join(path, f))]

    all_pictures = []
    pictures_info = []


    for picture_name in pictures:


        path = "Output/HD_pictures/"+picture_name
        picture = np.asarray(Image.open(path))

        max_x_dim = len(picture)
        max_y_dim = len(picture[0])
        dim = dim_start
        if dim > min(max_y_dim,max_x_dim):
            dim = min(max_y_dim,max_x_dim)

        if max_x_dim > max_y_dim:
            picture = np.transpose(picture, (1, 0, 2))

        max_x_dim = len(picture)
        max_y_dim = len(picture[0])
        xpos = 0
        ypos = 0
        now_Special = False
        stopper = 0

        while dim <= max_x_dim and dim <= max_y_dim:
            #print("Segmenting " + str(picture_name) + " in Dimention: " + str(dim))

            suffix = picture_name.replace(".png", "") + "/"
            suffix = suffix.replace("HD_", "")

            prefix = suffix.replace("/", "")

            newpath = "Output/sliced_and_resized/" + suffix  + prefix+ "_" + str(dim)
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            while (ypos <= max_y_dim - dim):
                xpos = 0
                while (xpos <= max_x_dim - dim):
                    segment = picture[xpos:xpos + dim, ypos:ypos + dim]

                    if not np.all(segment == segment[0][0]):
                        img = Image.fromarray(segment, 'RGB').resize((NN_dim,NN_dim))
                        img.save(newpath + "/" + str(prefix) + "_" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')

                        #img = np.asarray(img)
                        #all_pictures.append(img)
                        #pictures_info.append([xpos, ypos, dim])

                    xpos += int(dim * (1-overlap))

                # hanging picture at the end
                segment = picture[max_x_dim - dim:max_x_dim, ypos:ypos + dim]

                xpos = max_x_dim - dim
                if not np.all(segment == segment[0][0]):
                    img = Image.fromarray(segment, 'RGB').resize((NN_dim,NN_dim))
                    img.save(newpath + "/" + str(prefix) + "_" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')

                    #img = np.asarray(img)
                    #all_pictures.append(img)
                    #pictures_info.append([xpos, ypos, dim])


                ypos += int(dim * (1-overlap))

            # loop for hanging pictures at the side

            xpos = 0
            while (xpos <= max_x_dim - dim):
                segment = picture[xpos:xpos + dim, max_y_dim - dim:max_y_dim]
                ypos = max_y_dim - dim
                if not np.all(segment == segment[0][0]):
                    img = Image.fromarray(segment, 'RGB').resize((NN_dim,NN_dim))
                    img.save(newpath + "/" + str(prefix) + "_" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')

                    #img = np.asarray(img)
                    #all_pictures.append(img)
                    #pictures_info.append([xpos, ypos, dim])

                xpos += int(dim * (1-overlap))

            # hanging picture at the end on the side
            segment = picture[max_x_dim - dim:max_x_dim, max_y_dim - dim:max_y_dim]

            xpos = max_x_dim - dim
            ypos = max_y_dim - dim
            if not np.all(segment == segment[0][0]):
                img = Image.fromarray(segment, 'RGB').resize((NN_dim,NN_dim))
                img.save(newpath + "/" + str(prefix) + "_" + str(xpos) + "_" + str(ypos) + "_" + str(dim) + '.png')

                #img = np.asarray(img)
                #all_pictures.append(img)
                #pictures_info.append([xpos, ypos, dim])

            xpos += int(dim * (1-overlap))

            if now_Special is True:
                if int(stopper) == 1 or (dim == max_y_dim and dim == max_x_dim) :
                    break
                    #break
                leftover = max(max_y_dim, max_x_dim) - min(max_y_dim, max_x_dim)
                to_append = np.asarray([[[255, 255, 255] for x in range(max_y_dim)] for y in range(leftover)])
                picture = np.append(picture, to_append, axis=0)
                picture = picture.astype(np.uint8)
                max_y_dim = len(picture)
                max_x_dim = len(picture)
                now_Special = False

            #dim = int(dim_step * dim)
            dim = int(dim_step + dim)

            if dim > max_x_dim or dim > max_y_dim:
                dim = min(max_y_dim, max_x_dim)
                now_Special = True
                stopper += 0.5

            xpos = 0
            ypos = 0

    #return all_pictures, pictures_info


'''
# this is the special part

#do_special_images(file, max_y_dim, max_x_dim)

# this is the RESIZING

place = [x[0] for x in os.walk("Output/sliced_NON_resized/")]


t1 = time.time()
for old_folder in place:
    #print("resizing " + str(old_folder))
    new_folder = old_folder.replace("NON", "IS")
    files = [f for f in listdir(old_folder) if isfile(join(old_folder, f))]

    for file in files:
        #img = Image.open(old_folder + "/" + file)
        #img = img.resize((NN_dim, NN_dim))

        img = cv2.imread(old_folder + "/" + file, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (NN_dim, NN_dim))
        #if np.sum(np.asarray(img)) != 255*3*64*64 and np.sum(np.asarray(img)) != 0 and np.sum(np.asarray(img)) != color*3*64*64 :
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
            #img.save(new_folder + "/" + file)
        cv2.imwrite(new_folder + "/" + file, img)
print('rtesizxe time = ' + str(time.time() - t1))
'''






