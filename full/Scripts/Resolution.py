import math
import math
from copy import deepcopy
import numpy as np
import vg
import os


def Set_Resolution(file_source):
    def distance(p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        z1 = p1[2]
        x2 = p2[0]
        y2 = p2[1]
        z2 = p2[2]

        d = math.sqrt(math.pow(x2 - x1, 2) +
                      math.pow(y2 - y1, 2) +
                      math.pow(z2 - z1, 2) * 1.0)
        return d

    f = open(file_source, "r")
    g = f.read()
    f.close()

    num_lines = g.count('\n')
    num_facets = (num_lines - 2) / 7
    num_points = num_facets * 3
    lines = g.splitlines(0)
    lines_nospace = [lines[x].split() for x in range(len(lines))]
    all_points = []
    areas = []

    for x in range(int(num_facets)):
        pos = 1 + (7 * x)

        cur_p1 = [float(lines_nospace[pos + 2][1]), float(lines_nospace[pos + 2][2]), float(lines_nospace[pos + 2][3])]
        cur_p2 = [float(lines_nospace[pos + 3][1]), float(lines_nospace[pos + 3][2]), float(lines_nospace[pos + 3][3])]
        cur_p3 = [float(lines_nospace[pos + 4][1]), float(lines_nospace[pos + 4][2]), float(lines_nospace[pos + 4][3])]

        all_points.append([cur_p1, cur_p2, cur_p3])

        va = np.subtract(cur_p1, cur_p2)
        vb = np.subtract(cur_p1, cur_p3)
        cross = np.cross(va, vb)
        cur_area = 0.5 * ((cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2) ** 0.5)
        areas.append(cur_area)

    areas = sorted(areas)
    length = len(areas)
    step = int(length/10)
    totalA = sum(areas)
    proportions = []
    for x in range(10):
        summe = sum(areas[x*step:step*(x+1)-1])
        proportions.append(summe/totalA*100)
    if proportions[-1]>50:
        dim_start = 128
    else:
        dim_start = 64




    minimum_dist = math.inf
    for x in all_points:
        dist_between = [distance(x[0], x[1]), distance(x[0], x[2]), distance(x[2], x[1])]
        cur_dist = min(dist_between)
        if cur_dist < minimum_dist:
            minimum_dist = cur_dist

    max_x = -math.inf
    max_y = -math.inf
    max_z = -math.inf
    min_x = math.inf
    min_y = math.inf
    min_z = math.inf
    for f in range(len(all_points)):
        for g in range(3):
            xpos = all_points[f][g][0]
            ypos = all_points[f][g][1]
            zpos = all_points[f][g][2]
            if xpos > max_x:
                max_x = xpos
            if ypos > max_y:
                max_y = ypos
            if zpos > max_z:
                max_z = zpos

            if xpos < min_x:
                min_x = xpos
            if ypos < min_y:
                min_y = ypos
            if zpos < min_z:
                min_z = zpos

    x_dist = max_x - min_x
    y_dist = max_y - min_y
    z_dist = max_z - min_z

    maximum_dist = max(x_dist, y_dist, z_dist)
    resolution = int(maximum_dist / minimum_dist)

    return resolution, dim_start
