
import stltovoxel
import numpy as np


output = r"what.xyz"
resolution = 1000
array = np.zeros((resolution, resolution, resolution), dtype=np.uint8)
del array
stltovoxel.convert_file('hope.stl', 'output/output.png', resolution)

