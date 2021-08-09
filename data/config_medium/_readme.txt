
This folder contains STL files and pre-generated binvox-files for mediam configuration

Each stl-file contains only one feature. In total only 3 features are presented.

How to re-generate the binvox-files from stls-files

1. unzip stls-files
2. convert stls into binvox-files
3. move (copy) binvox-files into ./data/FNSet


As mentioned above, the binvox-files are already pre-generated,
so we can skip the previous step and just unzi the binvox.zip and move the unzipper binvox-files into ./data/FNSet

How to generate training and validation images

run the script generate_config_large.py


Which fils will be generated for training and validation sets

Binvox-files for training and for validation will be generated as a random combination of source-binvox-files.

Each random-generated binvox-file will contain exactly 2 Features (the same feature-type is allowed)

We will create fixed number of training set, but the combination of features is random,
so by each generation  (by each run of generate-script) we will get a different set of images