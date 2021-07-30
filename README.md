# SSD_EXT

The Solution contains two major parts (usages or activities)

- Training of the DNN
- Using DNN to recognize the features


Sources/References:

The DNN based on https://github.com/PeizhiShi/SsdNet.git



# Training


## How to create input files

To train and validate the DNN we need the input data. 

STLs are stored in data/STL/stls.rar

1. unzip stls.rar. Unzipped files to be placed into data/STl/stls
2. convert to binvox   (long running task aprox 24 hours)
3. copy binvox to ...
4. create minfo.csv  (only necessary if you add/delete some STLs). 
...
   
Prep Training set

run create_tr_set.py  (long running task approx 72 hours)


# Using of DNN

How to run (production, validation)

....






# Glossary

DNN - Deep Neural Network

SSD - single shot multibox detector
