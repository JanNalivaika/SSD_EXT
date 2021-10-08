
This folder contains STL files and pre-generated binvox-files for medium configuration

Each stl-file contains only one feature. In total only 3 features are presented.

How to re-generate the binvox-files from stls-files

1. unzip stls-files
2. convert stls into binvox-files
3. move (copy) binvox-files into ./data/FNSet


As mentioned above, the binvox-files are already pre-generated,
so we can skip the previous steps and just unzip the binvox.zip and move the unzipped binvox-files into ./data/FNSet


How to generate training and validation images

run the script generate_config_large.py


The Script will generate random input-files for training and validation sets

Binvox-files for training and for validation will be generated as a random combination of source-binvox-files.

Each random-generated binvox-file will contain exactly 2 Features (the same feature-type is allowed)

We will create fixed number of training images, but the combination of features is random,
so by each generation (by each run of generate-script) will create a different set of images.


Algorithm for creating random input files
1. Select random input-files (binvox)
2. Rotate randomly each input-file
3. Combine the files into one file