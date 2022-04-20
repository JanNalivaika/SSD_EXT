import torch
import numpy as np
import os
import pickle
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join



def Corrections():



    def soft_nms_pytorch(cur_boxes, sigma=0.5):

        # for each picture individually
        cur_boxes_new = np.zeros((0, 9))
        cur_boxes = np.asarray(cur_boxes)
        section = []
        pred_idx = 0
        pic_idx = cur_boxes[0][-1]
        while pred_idx < len(cur_boxes):

            if cur_boxes[pred_idx][-1] == pic_idx:
                # append
                slice = cur_boxes[pred_idx, :]
                section.append(slice)
                pred_idx += 1
            else:
                section = np.asarray(section)
                boxes = np.asarray(section[:, :6])
                box_scores = np.asarray(section[:, -2])

                # dets = boxes[:, 0:6].copy() * 1000
                dets = boxes[:, 0:6] * 1000

                N = dets.shape[0]

                indexes = torch.arange(0, N, dtype=torch.double).view(N, 1).cpu()
                dets = torch.from_numpy(dets).double().cpu()
                scores = torch.from_numpy(box_scores.copy()).double().cpu()

                dets = torch.cat((dets, indexes), dim=1).cpu()

                z1 = dets[:, 0]
                y1 = dets[:, 1]
                x1 = dets[:, 2]
                z2 = dets[:, 3]
                y2 = dets[:, 4]
                x2 = dets[:, 5]
                # scores = box_scores
                areas = (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

                for i in range(N):
                    tscore = scores[i].clone()
                    pos = i + 1

                    if i != N - 1:
                        maxscore, maxpos = torch.max(scores[pos:], dim=0)
                        if tscore < maxscore:
                            dets[i], dets[maxpos.item() + i + 1] = dets[maxpos.item() + i + 1].clone(), dets[i].clone()
                            scores[i], scores[maxpos.item() + i + 1] = scores[maxpos.item() + i + 1].clone(), scores[
                                i].clone()
                            areas[i], areas[maxpos + i + 1] = areas[maxpos + i + 1].clone(), areas[i].clone()

                    # IoU calculate
                    zz1 = np.maximum(dets[i, 0].to("cpu").numpy(), dets[pos:, 0].to("cpu").numpy())
                    yy1 = np.maximum(dets[i, 1].to("cpu").numpy(), dets[pos:, 1].to("cpu").numpy())
                    xx1 = np.maximum(dets[i, 2].to("cpu").numpy(), dets[pos:, 2].to("cpu").numpy())
                    zz2 = np.minimum(dets[i, 3].to("cpu").numpy(), dets[pos:, 3].to("cpu").numpy())
                    yy2 = np.minimum(dets[i, 4].to("cpu").numpy(), dets[pos:, 4].to("cpu").numpy())
                    xx2 = np.minimum(dets[i, 5].to("cpu").numpy(), dets[pos:, 5].to("cpu").numpy())

                    # w = np.maximum(0.0, xx2 - xx1 + 1)
                    # h = np.maximum(0.0, yy2 - yy1 + 1)
                    # l = np.maximum(0.0, zz2 - zz1 + 1)

                    w = np.asarray(xx2 - xx1 + 1)
                    h = np.asarray(yy2 - yy1 + 1)
                    l = np.asarray(zz2 - zz1 + 1)

                    inter = torch.tensor(w * h * l).cpu()
                    ovr = torch.div(inter, (areas[i] + areas[pos:] - inter)).cpu()

                    # Gaussian decay
                    weight = torch.exp(-(ovr * ovr) / sigma).cpu()

                    scores[pos:] = weight * scores[pos:]

                # print(scores)
                max_margin = 0
                thresh = 0
                for i in range(scores.shape[0] - 1):
                    if scores[i] - scores[i + 1] > max_margin:
                        max_margin = scores[i] - scores[i + 1]
                        thresh = (scores[i] + scores[i + 1]) / 2

                # thresh = (scores[1] + scores[2])/2

                keep = dets[:, 6][scores > thresh].int().to("cpu")
                keep = (np.array(keep)).astype(int)
                block = section[keep, :]
                cur_boxes_new = np.concatenate((cur_boxes_new, block), axis=0)

                pic_idx = cur_boxes[pred_idx][-1]
                section = []

        return cur_boxes_new


    def draw():
        HD_images = []
        HD_location = "Output\HD_pictures"
        HDfiles = [HD_location + "/" + f for f in listdir(HD_location) if isfile(join(HD_location, f))]

        upscaled = []

        for image in HDfiles:
            image = Image.open(image)
            image = np.array(image)
            HD_images.append(image)


        for prediction in predictions_raw:
            picture_index = int(prediction[8])
            #print(picture_index)
            mini_picture = onlyfiles[picture_index]
            mini_name = mini_picture.split("/")[-1].split("_")        #get hd picture
            HD_LOC = "Output\HD_pictures/HD_" + str(mini_name[0]) + "_" + str(mini_name[1]) + "_" + str(mini_name[2]) + ".png"
            HD_index =  HDfiles.index(HD_LOC)


            max_x_dim = HD_images[HD_index].shape[0]
            max_y_dim = HD_images[HD_index].shape[1]
            rec_scale = int(mini_name[-1].replace(".png", ""))
            scaler = rec_scale/64

            startposition_x = int(mini_name[-3])
            startposition_y = int(mini_name[-2])

            z1 = int(prediction[0] * scaler * 64)
            x1 = int(prediction[1] * scaler * 64) + startposition_x
            y1 = int(prediction[2] * scaler * 64) + startposition_y
            z2 = (int(prediction[3] * scaler * 64) - 1)
            x2 = (int(prediction[4] * scaler * 64) + startposition_x - 1)
            y2 = (int(prediction[5] * scaler * 64) + startposition_y - 1)
            Feature = prediction[6]
            prop = prediction[7]

            if x2>=max_x_dim:
                x2 = max_x_dim-1
            if y2>=max_y_dim:
                y2 = max_y_dim-1

            if x1>=max_x_dim or y1 >=max_y_dim or x1>=x2 or y1>=y2:
                continue


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

            color = np.asarray(color[0:3][::-1])
            HD_images[HD_index][x1][y1] = color
            HD_images[HD_index][x2][y2] = color

            for x in range(x2 - x1):
                HD_images[HD_index][x1 + x][y1] = color
                HD_images[HD_index][x1 + x][y2] = color

            for x in range(y2 - y1):
                HD_images[HD_index][x1][y1 + x] = color
                HD_images[HD_index][x2][y1 + x] = color

    predictions = pd.read_pickle('Output\sliced_and_resized/upscaled_predictions.pickle')
    new_pred = soft_nms_pytorch(predictions)