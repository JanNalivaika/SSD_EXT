# SSD_EXT

The Solution contains two major parts (usages or activities)

- Training of the DNN
- Using DNN to recognize the features


Sources/References:

The DNN based on https://github.com/PeizhiShi/SsdNet.git



# Training


## How to create input files

To train and validate the DNN we need the input data.

Three different environments/configurations are prepared.
The environments differ only by amount of input-files and amount of features in that files

### small configuration
In the folder **data/config_small** the input-files (PNGs) are already pre-generated.
Just for info and for completeness the source files STLs and Binvox are presented in corresponding folders
_data/config_small/binvox_ and _data/config_small/stl_.

We can use the script 'create_tr_set_small.py' to regenerate the PNGs from the BINVOX files
(for example in case if we want to change the set of input-files)

The presented the input-files contain only one feature - "through hole"

To use the input-PNG-files we need to place it into the folders _data/trset_ and _data/ValsSet_.
We can copy the files manually or just start the BATCH-file _data/config_small/prep_config.bat_


**_Still not described_** How to get BINVOX from STLs  (this info is available in next chapters)

### medium configuration
see readme.txt in the folder data/config_medium


### large configuration


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

 Segmentation of input PNG (if the size is bigger than 64x64)

 goal  - find large features on large input-pictures, i.e. no size limitation, for example the whole -diameter can be 1000 px


 Algorithm (incomplete/draft/general)

 * input-picture
 * test-picture
 * window-size
 * 64x64 - DNN Size

 1. resize the complete input-picture to 64x64 test-picture - run DNN and find the largest features (npy-like-file)
 2. resize the input-picture to 128x128 test-picture - do segmentation run DNN and detect features. compare/combine the features with prev test
 3. double the size and repeat step 2
 4. at some point (if any size of the input-picture is smaller than size of test-picture?) apply segmentation to the input-picture
 5. final result - show original input-picture (2D) with detected features

 Run DNN on all segments

 Re-Run DNN on 

....

 Block-Diagramm?




# Glossary

DNN - Deep Neural Network

SSD - single shot multibox detector
