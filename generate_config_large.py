from data import *
import os
import numpy as np
import csv
import matplotlib.pyplot as plt
import random

def create_training_set():
    #print("Change num_samples = 2900000")
    num_samples = 3_000_000

    random.seed(1024) # initialize the random number generator
    random_partition = create_partition_simple(3)

    list_IDs = random_partition['train']

    DIR = 'data/TrSet/'

    with open('data/minfo.csv', mode='r') as infile:
        reader = csv.reader(infile)
        list_size = {rows[0]:int(rows[1]) for rows in reader}

    counter = 1
    for idx in range(num_samples):
        rotation = int(idx%6)
        m_idx = int(idx/6)
        if rotation == 0:
            cur_model, cur_model_label, cur_model_components = achieve_random_model(list_IDs, list_size, DIR + str(counter))

        img, _ = create_img(cur_model, rotation, True)
        target = achieve_model_gt(cur_model_label, cur_model_components, rotation)

        if target.shape[0] == 0:
            continue

        print('processing the', idx, 'th image...')
        filename = DIR+str(counter)+str("_")+str(rotation)
        plt.imsave(filename+'.png',img,cmap='gray',vmin=0,vmax=255)


        np.save(filename+'.npy',target)
        counter = counter + 1


def test():
    tSet, vSet = create_partition_simple()
    print(len(tSet), len(vSet))



if __name__ == '__main__':
    #create_training_set()
    test()

