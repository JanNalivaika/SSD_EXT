import numpy as np
import csv
import utils.binvox_rw
from utils.augmentations import SSDAugmentation
from data import *
import torch
import torch.backends.cudnn as cudnn
from ssd import build_ssd
from torch.autograd import Variable
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pow
import matplotlib.patches as mpatches
import warnings
from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy as np

warnings.simplefilter("ignore", UserWarning)
import pickle

if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')


def get_gt_label(filename):
    retarr = np.zeros((0, 7))
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            items = row[0].split(',')
            retarr = np.insert(retarr, 0, np.asarray(items), 0)

    retarr[:, 0:6] = retarr[:, 0:6] * 1000

    return retarr


def load_pretrained_model():
    ssd_net = build_ssd(cfg['min_dim'], cfg['num_classes'])

    net = ssd_net

    net = torch.nn.DataParallel(ssd_net)
    cudnn.benchmark = True

    # ssd_net.load_weights('weights/512-exp2-notlda/VOC.pth')
    # ssd_net.load_weights('weights/VOCself5.pth')
    ssd_net.load_weights('Scripts/SSD/weights/VOCself6.pth')

    # print("Replace cup with cuda")
    return net.cuda()


def tensor_to_float(val):
    if val < 0:
        val = 0

    if val > 1:
        val = 1

    return float(val)




def soft_nms_pytorch(boxes, box_scores, sigma=0.5):
    dets = boxes[:, 0:6].copy() * 1000

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
                scores[i], scores[maxpos.item() + i + 1] = scores[maxpos.item() + i + 1].clone(), scores[i].clone()
                areas[i], areas[maxpos + i + 1] = areas[maxpos + i + 1].clone(), areas[i].clone()

        # IoU calculate
        zz1 = np.maximum(dets[i, 0].to("cpu").numpy(), dets[pos:, 0].to("cpu").numpy())
        yy1 = np.maximum(dets[i, 1].to("cpu").numpy(), dets[pos:, 1].to("cpu").numpy())
        xx1 = np.maximum(dets[i, 2].to("cpu").numpy(), dets[pos:, 2].to("cpu").numpy())
        zz2 = np.minimum(dets[i, 3].to("cpu").numpy(), dets[pos:, 3].to("cpu").numpy())
        yy2 = np.minimum(dets[i, 4].to("cpu").numpy(), dets[pos:, 4].to("cpu").numpy())
        xx2 = np.minimum(dets[i, 5].to("cpu").numpy(), dets[pos:, 5].to("cpu").numpy())

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        l = np.maximum(0.0, zz2 - zz1 + 1)
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

    keep = dets[:, 6][scores > thresh].int()

    # print(keep.shape)

    return keep.to("cpu").numpy()


def get_predictions(net):

    transform = SSDAugmentation(cfg['min_dim'], MEANS, phase='test')




    paths = []
    p1 = "Output/sliced_IS_resized"
    path_pos = [f.path for f in os.scandir(p1) if f.is_dir()]
    for x in path_pos:
        #p = x.repace("\\" ,"/")
        path_dim = [f.path for f in os.scandir(x) if f.is_dir()]
        paths = paths + path_dim

    for itr in range(len(paths)):
        path = paths[itr]
        print("Working on path " + str(itr) + " out of " + str(len(paths)))
        #path = "Output/sliced_IS_resized/top/top_800"
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

        images = []

        for image in onlyfiles:
            image = Image.open(path + "/" + image)
            img = np.negative(np.array(image))
            img, _, _ = transform(img, 0, 0)

            images.append(img)


        images = torch.tensor(images).permute(0, 3, 1, 2).float()

        # print("Replace cup with cuda")
        images = Variable(images.cuda())
        # images = images.cuda()

        out = net(images, 'test')
        # print("Replace cup with cuda")
        out.cuda()

        cur_boxes = np.zeros((0, 9))

        for i in range(len(out)):

            for j in range(out.shape[1]):
                label = out[i, j, 1].detach().cpu()

                if label == 0:
                    continue

                score = out[i, j, 0].detach().cpu()

                x1 = tensor_to_float(out[i, j, 2])
                y1 = tensor_to_float(out[i, j, 3])
                x2 = tensor_to_float(out[i, j, 4])
                y2 = tensor_to_float(out[i, j, 5])
                z1 = 0.0
                z2 = tensor_to_float(out[i, j, 6])

                if x1 >= x2 or y1 >= y2 or z2 <= 0:
                    continue

                a = z1
                b = y1
                c = x1
                d = z2
                e = y2
                f = x2

                cur_boxes = np.append(cur_boxes, np.array([a, b, c, d, e, f, label - 1, score, i]).reshape(1, 9), axis=0)


        with open(path + '/predictions.pickle', 'wb') as handle:
            pickle.dump(cur_boxes, handle, protocol=pickle.HIGHEST_PROTOCOL)


        keepidx = soft_nms_pytorch(cur_boxes[:, :7], cur_boxes[:, -1])
        cur_boxes = cur_boxes[keepidx, :]

        cur_boxes[:, 0:6] = 10000 * cur_boxes[:, 0:6]



def Recognize():
    net = load_pretrained_model()

    with torch.no_grad():
        with open(os.devnull, 'w') as devnull:

            get_predictions(net)




