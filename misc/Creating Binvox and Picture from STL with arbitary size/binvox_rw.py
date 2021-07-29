import numpy as np


class Voxels(object):

    def __init__(self, data, dims, translate, scale, axis_order):
        a = data
        self.data = data
        self.dims = dims
        self.translate = translate
        self.scale = scale
        assert (axis_order in ('xzy', 'xyz'))
        self.axis_order = axis_order

    def clone(self):
        data = self.data.copy()
        dims = self.dims[:]
        translate = self.translate[:]
        return Voxels(data, dims, translate, self.scale, self.axis_order)

    def write(self, fp):
        write(self, fp)


def write(voxel_model, fp):
    data = voxel_model.data
    len_x, len_y, len_z = len(data), len(data[0]), len(data[0][0])
    fp.write(b'#binvox 1\n')
    fp.write(('dim ' + str(len_x) + ' ' + str(len_y) + ' ' + str(len_z) + '\n').encode('utf-8'))
    fp.write(b'translate 0 0 0\n')
    fp.write(b'scale 10\n')
    fp.write(b'data\n')

    state = data[0][0][0]
    ctr = 0
    for x in range(len_x):  # depth from back to front
        for y in range(len_y):  # from bottom to top
            for z in range(len_z):
                val = data[x][y][z]

                if val == state:
                    ctr += 1
                    #print(ctr)
                    # if ctr hits max, dump
                    if ctr == len_z:
                        fp.write(chr(state).encode('ascii'))
                        fp.write(chr(ctr).encode('ascii'))
                        ctr = 0
                else:
                    # if switch state, dump
                    fp.write(chr(state).encode('ascii'))
                    fp.write(chr(ctr).encode('ascii'))
                    state = val
                    ctr = 1
            # flush out remainders
    if ctr > 0:
        fp.write(chr(state).encode('ascii'))
        fp.write(chr(ctr).encode('ascii'))




