import math
from copy import deepcopy
import numpy as np
import vg
import os


def turnSTL(file_source):

    output_path = r'Output/STLs'
    if not os.path.exists(output_path):
        os.makedirs(output_path)


    f = open(file_source, "r")
    g = f.read()
    f.close()

    f = open("Output/STLs/0.stl", "w")
    f.write(g)
    f.close()

    # print(g)
    num_lines = g.count('\n')
    num_facets = (num_lines - 2) / 7
    num_points = num_facets * 3
    lines = g.splitlines(0)
    lines_nospace = [lines[x].split() for x in range(len(lines))]
    unique_vectors = []
    all_vectors = []
    all_points = []
    areas = []

    for x in range(int(num_facets)):
        pos = 1 + (7 * x)
        cur_vector_normal = [float(lines_nospace[pos][2]), float(lines_nospace[pos][3]), float(lines_nospace[pos][4])]

        cur_vector_normal = [round(num, 3) for num in cur_vector_normal]

        cur_p1 = [float(lines_nospace[pos + 2][1]), float(lines_nospace[pos + 2][2]), float(lines_nospace[pos + 2][3])]
        cur_p2 = [float(lines_nospace[pos + 3][1]), float(lines_nospace[pos + 3][2]), float(lines_nospace[pos + 3][3])]
        cur_p3 = [float(lines_nospace[pos + 4][1]), float(lines_nospace[pos + 4][2]), float(lines_nospace[pos + 4][3])]

        all_points.append([cur_p1, cur_p2, cur_p3])

        va = np.subtract(cur_p1, cur_p2)
        vb = np.subtract(cur_p1, cur_p3)
        cross = np.cross(va, vb)
        cur_area = 0.5 * ((cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2) ** 0.5)

        all_vectors.append(cur_vector_normal)

        if cur_vector_normal not in unique_vectors:
            inverse_v = [-x for x in cur_vector_normal]
            if inverse_v not in unique_vectors:
                unique_vectors.append(cur_vector_normal)
                areas.append(cur_area)
            else:
                value_index = unique_vectors.index(inverse_v)
                areas[value_index] += cur_area

        else:
            value_index = unique_vectors.index(cur_vector_normal)
            areas[value_index] += cur_area

    areas, unique_vectors = zip(*sorted(zip(areas, unique_vectors)))

    status = []
    for x in range(len(unique_vectors)):
        round_prec = 3
        a = round(unique_vectors[x][0], round_prec)
        b = round(unique_vectors[x][1], round_prec)
        c = round(unique_vectors[x][2], round_prec)
        if 2 == unique_vectors[x].count(0):
            # is facing a axis
            status.append(True)
        else:
            # pointing randomly in space
            status.append(False)

    area_to_axis = 0
    area_NOT_to_axis = 0
    total_area = 0

    for x in range(len(unique_vectors)):
        total_area += areas[x]
        if status[x]:
            area_to_axis += areas[x]
        else:
            area_NOT_to_axis += areas[x]

    #print(area_to_axis / total_area * 100)
    #print(area_NOT_to_axis / total_area * 100)

    wrong_vectors = [i for i, x in enumerate(status) if x == False]
    wrong_areas_pers = []
    for x in wrong_vectors:
        wrong_areas_pers.append(areas[x] / area_NOT_to_axis)

    # for selecting angle
    x_ax = [1, 0, 0]
    z_ax = [0, 0, 1]

    angles_for_turning = []
    for idx, pos in enumerate(wrong_vectors):
        if wrong_areas_pers[idx] > 0.1:
            vector = unique_vectors[pos]

            dot = np.dot(x_ax, vector)  # dot product
            det = -vector[1]  # determinant
            x_angle = np.arctan2(det, dot)

            dot = np.dot(z_ax, vector)  # dot product
            det = vector[1]  # determinant
            z_angle = np.arctan2(det, dot)

            z_angle = -vg.angle(np.array(z_ax), np.array(vector))*0.01745329252

            turning_vec = [x_angle, z_angle]

            angles_for_turning.append(turning_vec)


    for x in range(len(angles_for_turning)):
        for y in range(2):
            tester = round(angles_for_turning[x][y], 4)
            tester1 = round(angles_for_turning[x][0], 4)
            tester2 = round(angles_for_turning[x][1], 4)
            pi = round(math.pi,4)
            if tester == pi or tester == -pi:
                angles_for_turning[x][y] = 0
            if tester == -pi/2:
                angles_for_turning[x][y] = math.pi / 2


    angles_for_turning = [elem for elem in angles_for_turning if elem != [0, 0]]

    with open('Output/STLs/angles_for_turning.npy', 'wb') as f:
        np.save(f, angles_for_turning)


    for chosen in range(len(angles_for_turning)):
        angleXY = angles_for_turning[-chosen][0]
        angleZX = angles_for_turning[-chosen][1]
        # ngleXY = 0
        # angleZX = -math.pi/6

        all_vectors_new = deepcopy(all_vectors)
        all_points_new = deepcopy(all_points)

        for x in range(len(all_vectors)):
            # changing normals
            x_pos, y_pos, z_pos = all_vectors[x][0], all_vectors[x][1], all_vectors[x][2]

            # turning around Z
            new_z_temp = z_pos
            new_x_temp = math.cos(angleXY) * x_pos - math.sin(angleXY) * y_pos
            new_y_temp = math.sin(angleXY) * x_pos + math.cos(angleXY) * y_pos

            # turning around Y
            new_y = new_y_temp
            new_x = math.cos(angleZX) * new_x_temp - math.sin(angleZX) * new_z_temp
            new_z = math.sin(angleZX) * new_x_temp + math.cos(angleZX) * new_z_temp

            all_vectors_new[x][0], all_vectors_new[x][1], all_vectors_new[x][2] = new_x, new_y, new_z

            for y in range(3):
                # Changing points
                x_pos, y_pos, z_pos = all_points[x][y][0], all_points[x][y][1], all_points[x][y][2]

                # turning around Z
                new_z_temp = z_pos
                new_x_temp = math.cos(angleXY) * x_pos - math.sin(angleXY) * y_pos
                new_y_temp = math.sin(angleXY) * x_pos + math.cos(angleXY) * y_pos

                # turning around Y
                new_y = new_y_temp
                new_x = math.cos(angleZX) * new_x_temp - math.sin(angleZX) * new_z_temp
                new_z = math.sin(angleZX) * new_x_temp + math.cos(angleZX) * new_z_temp

                all_points_new[x][y][0], all_points_new[x][y][1], all_points_new[x][y][2] = new_x, new_y, new_z

        # replacing elements
        lines_nospace_new = deepcopy(lines_nospace)

        for x in range(int(num_facets)):
            pos = 1 + (7 * x)
            lines_nospace_new[pos][2] = str(all_vectors_new[x][0])
            lines_nospace_new[pos][3] = str(all_vectors_new[x][1])
            lines_nospace_new[pos][4] = str(all_vectors_new[x][2])

            pos_v1 = 3 + (7 * x)
            lines_nospace_new[pos_v1][1] = str(all_points_new[x][0][0])
            lines_nospace_new[pos_v1][2] = str(all_points_new[x][0][1])
            lines_nospace_new[pos_v1][3] = str(all_points_new[x][0][2])

            pos_v2 = 4 + (7 * x)
            lines_nospace_new[pos_v2][1] = str(all_points_new[x][1][0])
            lines_nospace_new[pos_v2][2] = str(all_points_new[x][1][1])
            lines_nospace_new[pos_v2][3] = str(all_points_new[x][1][2])

            pos_v3 = 5 + (7 * x)
            lines_nospace_new[pos_v3][1] = str(all_points_new[x][2][0])
            lines_nospace_new[pos_v3][2] = str(all_points_new[x][2][1])
            lines_nospace_new[pos_v3][3] = str(all_points_new[x][2][2])

        for x in range(len(lines_nospace_new)):
            lines_nospace_new[x] = " ".join(str(item) for item in lines_nospace_new[x])

        finish = "\n".join(str(item) for item in lines_nospace_new)

        f = open("Output/STLs/" + str(chosen+1) + ".stl", "w")
        f.write(finish)
        f.close()



