import math
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from . import perimeter
import pickle
import os


def mesh_to_plane(output_file_path, mesh, bounding_box, parallel, resolution):
    if parallel:
        pool = mp.Pool(mp.cpu_count())
        result_ids = []

    # Note: vol should be addressed with vol[z][y][x]
    #vol = np.zeros(bounding_box[::-1], dtype=bool)
    vol = np.zeros([resolution,resolution], dtype=bool)
    current_mesh_indices = set()
    z = 0
    BOOL = []
    for event_z, status, tri_ind in generate_tri_events(mesh):
        while event_z - z >= 0:
            mesh_subset = [mesh[ind] for ind in current_mesh_indices]
            if parallel:
                result_id = pool.apply_async(paint_z_plane, args=(mesh_subset, z, bounding_box[:2]))
                result_ids.append(result_id)
            else:
                print('Processing layer %d/%d' % (z, bounding_box[2]))
                _, pixels = paint_z_plane(mesh_subset, z, bounding_box[:2])
                #vol[z] = pixels
                if z > 0:
                    plt.imsave(output_file_path+str(z) + '.png', pixels, cmap=cm.gray)
                    BOOL.append(pixels)
            z += 1



        if status == 'start':
            assert tri_ind not in current_mesh_indices
            current_mesh_indices.add(tri_ind)
        elif status == 'end':
            assert tri_ind in current_mesh_indices
            current_mesh_indices.remove(tri_ind)

    output_path = r'Output/Combined_Voxel'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open("Output/Combined_Voxel/VoxelizedSTL.pickle", 'wb') as handle:
        pickle.dump(BOOL, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if parallel:
        results = [r.get() for r in result_ids]

        for z, pixels in results:
            vol[z] = pixels

        pool.close()
        pool.join()

    return vol


def paint_z_plane(mesh, height, plane_shape):
    pixels = np.zeros(plane_shape, dtype=bool)

    lines = []
    for triangle in mesh:
        triangle_to_intersecting_lines(triangle, height, pixels, lines)
    perimeter.lines_to_voxels(lines, pixels)

    return height, pixels


def linear_interpolation(p1, p2, distance):
    '''
    :param p1: Point 1
    :param p2: Point 2
    :param distance: Between 0 and 1, Lower numbers return points closer to p1.
    :return: A point on the line between p1 and p2
    '''
    return p1 * (1-distance) + p2 * distance


def triangle_to_intersecting_lines(triangle, height, pixels, lines):
    assert (len(triangle) == 3)
    above = list(filter(lambda pt: pt[2] > height, triangle))
    below = list(filter(lambda pt: pt[2] < height, triangle))
    same = list(filter(lambda pt: pt[2] == height, triangle))
    if len(same) == 3:
        for i in range(0, len(same) - 1):
            for j in range(i + 1, len(same)):
                lines.append((same[i], same[j]))
    elif len(same) == 2:
        lines.append((same[0], same[1]))
    elif len(same) == 1:
        if above and below:
            side1 = where_line_crosses_z(above[0], below[0], height)
            lines.append((side1, same[0]))
        else:
            x = int(same[0][0])
            y = int(same[0][1])
            pixels[y][x] = True
    else:
        cross_lines = []
        for a in above:
            for b in below:
                cross_lines.append((b, a))
        side1 = where_line_crosses_z(cross_lines[0][0], cross_lines[0][1], height)
        side2 = where_line_crosses_z(cross_lines[1][0], cross_lines[1][1], height)
        lines.append((side1, side2))


def where_line_crosses_z(p1, p2, z):
    if (p1[2] > p2[2]):
        p1, p2 = p2, p1
    # now p1 is below p2 in z
    if p2[2] == p1[2]:
        distance = 0
    else:
        distance = (z - p1[2]) / (p2[2] - p1[2])
    return linear_interpolation(p1, p2, distance)


def calculate_scale_shift(meshes, resolution):
    mesh_min = meshes[0].min(axis=(0, 1))
    mesh_max = meshes[0].max(axis=(0, 1))
    for mesh in meshes[1:]:
        mesh_min = np.minimum(mesh_min, mesh.min(axis=(0, 1)))
        mesh_max = np.maximum(mesh_max, mesh.max(axis=(0, 1)))

    amplitude = mesh_max - mesh_min
    # Floating point errors can creep in here. Ex: 25 * 1.16 = 28.999999999999996
    # Need to be careful about when numbers are divided.
    xy_scale = (resolution - 1) / max(amplitude[:2])
    z_resolution = amplitude[2] * (resolution - 1) / max(amplitude[:2])

    z_resolution = math.floor(z_resolution) + 1
    bounding_box = [resolution, resolution, z_resolution]
    return xy_scale, mesh_min, bounding_box


def scale_and_shift_mesh(mesh, scale, shift):
    for i, dim_shift in enumerate(shift):
        mesh[..., i] = (mesh[..., i] - dim_shift) * scale


def generate_tri_events(mesh):
    # Create data structure for plane sweep
    events = []
    for i, tri in enumerate(mesh):
        bottom, middle, top = sorted(tri, key=lambda pt: pt[2])
        events.append((bottom[2], 'start', i))
        events.append((top[2], 'end', i))
    return sorted(events, key=lambda tup: tup[0])
