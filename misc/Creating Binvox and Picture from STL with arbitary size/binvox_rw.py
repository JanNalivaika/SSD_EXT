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
                        fp.write(chr(state).encode('utf-8'))
                        fp.write(chr(ctr).encode('utf-8'))
                        ctr = 0
                else:
                    # if switch state, dump
                    fp.write(chr(state).encode('utf-8'))
                    fp.write(chr(ctr).encode('utf-8'))
                    state = val
                    ctr = 1
            # flush out remainders
    if ctr > 0:
        fp.write(chr(state).encode('utf-8'))
        fp.write(chr(ctr).encode('utf-8'))


def read_header(fp):
    """ Read binvox header. Mostly meant for internal use.
    """
    line = fp.readline().strip()
    if not line.startswith(b'#binvox'):
        raise IOError('Not a binvox file')
    dims = list(map(int, fp.readline().strip().split(b' ')[1:]))
    translate = list(map(float, fp.readline().strip().split(b' ')[1:]))
    scale = list(map(float, fp.readline().strip().split(b' ')[1:]))[0]
    line = fp.readline()
    return dims, translate, scale


def read_as_3d_array(fp, fix_coords=True):
    """ Read binary binvox format as array.
    Returns the model with accompanying metadata.
    Voxels are stored in a three-dimensional numpy array, which is simple and
    direct, but may use a lot of memory for large models. (Storage requirements
    are 8*(d^3) bytes, where d is the dimensions of the binvox model. Numpy
    boolean arrays use a byte per element).
    Doesn't do any checks on input except for the '#binvox' line.
    """
    dims, translate, scale = read_header(fp)
    raw_data = np.frombuffer(fp.read(), dtype=np.uint8)
    # if just using reshape() on the raw data:
    # indexing the array as array[i,j,k], the indices map into the
    # coords as:
    # i -> x
    # j -> z
    # k -> y
    # if fix_coords is true, then data is rearranged so that
    # mapping is
    # i -> x
    # j -> y
    # k -> z
    values, counts = raw_data[::2], raw_data[1::2]
    dim3 = max(counts)
    pix1 = dims[0]*dims[1]*dims[2]
    pix = sum(counts)
    data = np.repeat(values, counts).astype(np.bool)
    data = data.reshape(dims)
    if fix_coords:
        # xzy to xyz TODO the right thing
        data = np.transpose(data, (0, 2, 1))
        axis_order = 'xyz'
    else:
        axis_order = 'xzy'
    return Voxels(data, dims, translate, scale, axis_order)
