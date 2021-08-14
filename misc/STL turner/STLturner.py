import math
from copy import deepcopy
import numpy as np


f = open("turnedinspace2.stl", "r")
g = f.read()
# print(g)
num_lines = g.count('\n')
num_facets = (num_lines - 2) / 7
num_points = num_facets * 3
lines = g.splitlines(0)
lines_nospace = [lines[x].split() for x in range(len(lines))]
unique_vectors = []
all_vectors =[]
all_points =[]
areas = []

for x in range(int(num_facets)):
    pos = 1 + (7 * x)
    cur_vector = [float(lines_nospace[pos][2]) , float(lines_nospace[pos][3]) , float(lines_nospace[pos][4])]

    v1 = [float(lines_nospace[pos + 2][1]), float(lines_nospace[pos + 2][2]), float(lines_nospace[pos + 2][3])]
    v2 = [float(lines_nospace[pos + 3][1]), float(lines_nospace[pos + 3][2]), float(lines_nospace[pos + 3][3])]
    v3 = [float(lines_nospace[pos + 4][1]), float(lines_nospace[pos + 4][2]), float(lines_nospace[pos + 4][3])]

    all_points.append([v1,v2,v3])

    va = np.subtract(v1, v2)
    vb = np.subtract(v1, v3)
    cross = np.cross(va, vb)
    area = 0.5 * ((cross[0]**2 + cross[1]**2 + cross[2]**2)**0.5)

    all_vectors.append(cur_vector)

    if cur_vector not in unique_vectors:
        unique_vectors.append(cur_vector)
        areas.append(area)
    else:
        value_index = unique_vectors.index(cur_vector)
        areas[value_index] += area

areas, unique_vectors = zip(*sorted(zip(areas, unique_vectors)))



status = []
for x in range(len(unique_vectors)):
    a = unique_vectors[x][0]
    b = unique_vectors[x][1]
    c = unique_vectors[x][2]
    if (a+b) ==0 or  (b+c) == 0 or (c+a) == 0:
        status.append(True)
    else:
        status.append(False)

area_to_axis = 0
area_NOT_to_axis = 0
total_area = 0
for x in range(len(unique_vectors)):
    total_area += areas[x]
    if status[x]:
        area_to_axis += areas[x]
    else:
        area_NOT_to_axis+=areas[x]

print(area_to_axis/total_area*100)
print(area_NOT_to_axis/total_area*100)

wrong_vectors = [i for i, x in enumerate(status) if x == False]

# for selecting angle
x_ax = [1,0,0]
y_ax = [0,1,0]
z_ax = [0,0,1]


print("SELECT THE RIGHT VecTOR")
# 49,48,47,44
vector = unique_vectors[49]
"""dot_product = np.dot( x_ax,vector)
angle = np.arccos(dot_product) * 180 / math.pi
angle = np.arctan2(dot_product) # why minus ???????????????????????????
angle = np.sign(vector[0]) * np.sign(vector[1]) * angle"""

dot = np.dot( x_ax,vector)     # dot product
det = -vector[1]      # determinant
angle = np.arctan2(det, dot)

print("make sure plus or minus !!!!!!")
# rotate around Z == x and y change

all_vectors_new = deepcopy(all_vectors)
all_points_new = deepcopy(all_points)

for x in range(len(all_vectors)):
    #changing normals
    x_pos, y_pos = all_vectors[x][0], all_vectors[x][1]
    new_x = math.cos(angle) * x_pos - math.sin(angle) * y_pos
    new_y = math.sin(angle) * x_pos + math.cos(angle) * y_pos

    all_vectors_new[x][0], all_vectors_new[x][1] = new_x, new_y


    for y in range(3):
        #Changing points
        x_pos, y_pos = all_points[x][y][0], all_points[x][y][1]
        new_x = math.cos(angle) * x_pos - math.sin(angle) * y_pos
        new_y = math.sin(angle) * x_pos + math.cos(angle) * y_pos

        all_points_new[x][y][0], all_points_new[x][y][1] = new_x, new_y


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

f = open("hope.stl", "w")
f.write(finish)
f = open("../Creating Binvox and Picture from STL with arbitary size/testing/hope.stl", "w")
f.write(finish)
pass
