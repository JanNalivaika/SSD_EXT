import os
import glob
import sys


def splitt_file(filename, chunk_size):
    file_number = 1
    with open(filename, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            with open(filename + '.' + str(file_number), 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunk_size)


def merge_files(pattern, target):
    files = glob.glob(pattern)
    with open(target, 'ab') as outfile:
        for file in files:
            with open(file, 'rb') as f:
                outfile.write(f.read())


def remove_files(folder, pattern):
    files = glob.glob(folder + '/' + pattern, recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def create_weights():
    file_weights = 'weights/VOC.pth'
    flag = os.path.isfile(file_weights)
    if flag:
        return

    file_weights_pattern = 'weights/voc.pth.*'
    merge_files(file_weights_pattern, file_weights);


# called from dockerfile to create voc.pth
if __name__ == "__main__":
    create_weights()
    remove_files('weights', 'voc.pth.*')
