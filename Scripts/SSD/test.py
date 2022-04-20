import csv
from .utils.augmentations import SSDAugmentation
from .data import *
import torch
import torch.backends.cudnn as cudnn
from .ssd import build_ssd
from torch.autograd import Variable
import warnings
from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy as np
import time
import glob

warnings.simplefilter("ignore", UserWarning)
import pickle

if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')

WEIGHTS_FOLDER = "Scripts/SSD/weights/"


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
    ssd_net.load_weights(WEIGHTS_FOLDER + 'VOC.pth')

    # print("Replace cup with cuda")
    return net.cuda() if (torch.cuda.is_available()) else net.cpu()


def tensor_to_float(val):
    if val < 0:
        val = 0

    if val > 1:
        val = 1

    return float(val)


def soft_nms_pytorch(cur_boxes, sigma=0.5):

    # for each picture individually
    cur_boxes_new = np.zeros((0, 9))
    cur_boxes = np.asarray(cur_boxes)
    section = []
    pred_idx = 0
    pic_idx = cur_boxes[0][-1]
    while pred_idx < len(cur_boxes):

        if cur_boxes[pred_idx][-1] == pic_idx:
            #append
            slice = cur_boxes[pred_idx, :]
            section.append(slice)
            pred_idx += 1
        else:
            section = np.asarray(section)
            boxes =  np.asarray(section[:,:6])
            box_scores =  np.asarray(section[:, -2])


            #dets = boxes[:, 0:6].copy() * 1000
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
                        scores[i], scores[maxpos.item() + i + 1] = scores[maxpos.item() + i + 1].clone(), scores[i].clone()
                        areas[i], areas[maxpos + i + 1] = areas[maxpos + i + 1].clone(), areas[i].clone()

                # IoU calculate
                zz1 = np.maximum(dets[i, 0].to("cpu").numpy(), dets[pos:, 0].to("cpu").numpy())
                yy1 = np.maximum(dets[i, 1].to("cpu").numpy(), dets[pos:, 1].to("cpu").numpy())
                xx1 = np.maximum(dets[i, 2].to("cpu").numpy(), dets[pos:, 2].to("cpu").numpy())
                zz2 = np.minimum(dets[i, 3].to("cpu").numpy(), dets[pos:, 3].to("cpu").numpy())
                yy2 = np.minimum(dets[i, 4].to("cpu").numpy(), dets[pos:, 4].to("cpu").numpy())
                xx2 = np.minimum(dets[i, 5].to("cpu").numpy(), dets[pos:, 5].to("cpu").numpy())

                #w = np.maximum(0.0, xx2 - xx1 + 1)
                #h = np.maximum(0.0, yy2 - yy1 + 1)
                #l = np.maximum(0.0, zz2 - zz1 + 1)

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
            block = section[keep,:]
            cur_boxes_new = np.concatenate((cur_boxes_new, block), axis=0)

            pic_idx = cur_boxes[pred_idx][-1]
            section = []

    return cur_boxes_new


def get_predictions(net):
    transform = SSDAugmentation(cfg['min_dim'], MEANS, phase='test')

    paths = []
    p1 = "Output/sliced_and_resized"
    filelist = []
    onlyfiles = []

    #for root, dirs, files in os.walk(p1):
    #    for file in files:
    #        filelist.append(os.path.join(root, file))
    #estimated_time = len(filelist) / 4
    #print("estmated time " + str(estimated_time) + " seconds")

    path_pos = [f.path for f in os.scandir(p1) if f.is_dir()]
    for x in path_pos:
        # p = x.repace("\\" ,"/")
        path_dim = [f.path for f in os.scandir(x) if f.is_dir()]
        paths = paths + path_dim

    for itr in range(len(paths)):
        path = paths[itr]
        #print("Working Recognition on path " + str(itr) + " out of " + str(len(paths)))
        t = time.time()
        # path = "Output/sliced_IS_resized/top/top_800"
        #onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        onlyfiles.extend([path + "/" + f for f in listdir(path) if isfile(join(path, f))])

    images = []
    t1 = time.time()
    for image in onlyfiles:
        image = Image.open(image)
        temp = np.array(image)
        img, _, _ = transform(temp, 0, 0)
        images.append(img)
    print("     Appending images Time: " + str(time.time() - t1))

    t1 = time.time()
    images = np.asarray(images)
    images = torch.tensor(images)
    print("     converting images to tensor Time: " + str(time.time() - t1))

    t1 = time.time()
    images = images.permute(0, 3, 1, 2)
    print("     permutation images : " + str(time.time() - t1))

    t1 = time.time()
    images = images.float()
    print("     converting images to float: " + str(time.time() - t1))

    # print("Replace cup with cuda")
    t1 = time.time()
    images = Variable(images.cuda() if (torch.cuda.is_available()) else images.cpu())
    print("     Pushing images to device Time: " + str(time.time() - t1))
    t1 = time.time()
    out = net(images, 'test')
    del images
    print("     Running images trough NN Time: " + str(time.time() - t1))

    # print("Replace cup with cuda")
    t1 = time.time()
    # out.cuda() if (torch.cuda.is_available()) else out.cpu()
    out = out.cpu().numpy()
    print("     Pushing output to CPU Time: " + str(time.time() - t1))

    cur_boxes = np.zeros((0, 9))
    t1 = time.time()
    for i in range(len(out)):

        pred = out[i, :, :] # getting prediction block for 1 picture
        pred = np.delete(pred, np.where(pred[:,1] == 0)[0], axis=0)  # deleting all empty predictions

        pred = np.delete(pred, np.where(pred[:, 2] >= pred[:, 4])[0], axis=0)  # deleting wrong x
        pred = np.delete(pred, np.where(pred[:, 3] >= pred[:, 5])[0], axis=0)  # deleting wrong y
        pred = np.delete(pred, np.where(pred[:, 1] <= 0)[0], axis=0)  # deleting wrong z

        pred = pred.astype(float)
        pred[:,2:7] = np.where(pred[:,2:7] < 0, 0, pred[:,2:7])  # normalizing out of bound predictions
        pred[:,2:7] = np.where(pred[:, 2:7] > 1, 1, pred[:, 2:7])  # normalizing out of bound predictions
        pred[:, 1] = pred[:, 1]-1
        pic_num = np.ones((pred.shape[0], 1)) * i
        z_app = np.zeros((pred.shape[0], 1))
        pred = np.concatenate((pred, z_app), axis=1)
        pred = np.concatenate((pred, pic_num), axis=1)
        cur_boxes = np.concatenate((cur_boxes, pred), axis=0)



        """
        for j in range(out.shape[1]):

            # label = out[i, j, 1].detach().cpu()
            #label = out[i, :, 1]

            if label == 0:
                continue

            # score = out[i, j, 0].detach().cpu()
            score = out[i, j, 0]

            slice = out[i, j, 2:7].astype(float)
            slice = np.where(slice < 0, 0, slice)
            slice = np.where(slice > 1, 1, slice)

            # x1 = tensor_to_float(out[i, j, 2])
            # y1 = tensor_to_float(out[i, j, 3])
            # x2 = tensor_to_float(out[i, j, 4])
            # y2 = tensor_to_float(out[i, j, 5])
            # z2 = tensor_to_float(out[i, j, 6])
            z1 = 0.0

            [x1, y1, x2, y2, z2] = slice
            if x1 >= x2 or y1 >= y2 or z2 <= 0:
                continue

            cur_boxes = np.append(cur_boxes, np.array([z1, y1, x1, z2, y2, x2, label - 1, score, i]).reshape(1, 9),
                                  axis=0)
        """

    print("     Tensor to float Time: " + str(time.time() - t1))
    # 2000 img = 14.017673254013062
    # with numpy = 1.3463826179504395
    # with giga optimization ==  0.255

    # print("Pay attention here")
    t1 = time.time()
    # atm =       [score , lable, x1, y1, x2, y2,    z2,    z1, i]
    # must be =   [    z1,    y1, x1, z2, y2, x2, label, score, i]
    cur_boxes = cur_boxes[:, [7, 3, 2, 6, 5, 4, 1, 0, 8]]
    cur_boxes = soft_nms_pytorch(cur_boxes)
    #cur_boxes = cur_boxes[keepidx, :]
    #origimal time = 4
    #print("soft_nms Time: " + str(time.time() - t1))

    t1 = time.time()
    with open(p1 + '/predictions.pickle', 'wb') as handle:
        pickle.dump(cur_boxes, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #print("pickle dumping Time: " + str(time.time() - t1))

    # cur_boxes[:, 0:6] = 10000 * cur_boxes[:, 0:6]

    #print(
    #    "Recognition on path " + str(itr) + " took " + str(
    #        int(time.time() - t)) + " seconds.   That equals to: " + str(int(
    #        len(onlyfiles) / (time.time() - t))) + " pic/sec    Analyzed pictures: " + str(len(onlyfiles)))
    #pass

def Recognize():
    create_weights()
    t1 = time.time()
    net = load_pretrained_model()
    #print("Net loading Time Time: " + str(time.time() - t1))
    with torch.no_grad():
        with open(os.devnull, 'w') as devnull:
            get_predictions(net)


def create_weights():
    #
    file_weights = WEIGHTS_FOLDER + 'VOC.pth'
    flag = os.path.isfile(file_weights)
    if flag:
        return

    import zipfile

    zips = glob.glob(WEIGHTS_FOLDER + 'VOC.zip.*')
    target = os.path.relpath(WEIGHTS_FOLDER + "voc.zip")
    for zipName in zips:
        source = zipName
        with open(target, "ab") as f:
            with open(source, "rb") as z:
                f.write(z.read())

    zip_ref = zipfile.ZipFile(target, "r")
    zip_ref.extractall(WEIGHTS_FOLDER)
