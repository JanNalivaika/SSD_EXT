import numpy as np
import os
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math
import binvox_rw
from PIL import Image
import time

def MakeAPicture(block):
    w, h = len(block), len(block[0])
    data = np.zeros((w, h, 3), dtype=np.uint8)
    depth = len(block[0][0])
    inc = 255/depth

    for x in range(depth):
        for x in range(len(data)):
            for y in range(len(data[0])):
                if int(block[x][y][z]) != 1:
                    data[x][y][0] += inc
                    data[x][y][1] += inc
                    data[x][y][2] += inc


    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()

    pass





def SAVEasBINVOX(block):
    newfile = open('NEW.binvox', 'wb')
    block = block.tolist()
    for x in range(len(block)):
        for y in range(len(block[0])):
            for z in range(len(block[0][0])):
                if int(block[x][y][z]) == 1:
                    block[x][y][z] = True
                else:
                    block[x][y][z] = False

    dims = [len(block), len(block[0]), len(block[0][0])]
    translate = 0
    scale = 10
    axis_order = 'xyz'
    m2 = binvox_rw.Voxels(block, dims, translate, scale, axis_order)
    m2.write(newfile)


## define functions
def triangle_voxalize(triangle):
    trix = []
    triy = []
    triz = []
    triangle = list(triangle)

    # corners of triangle in array formats
    p0 = np.array(triangle[0])
    p1 = np.array(triangle[1])
    p2 = np.array(triangle[2])

    # vectors and the plane of the triangle
    v0 = p1 - p0
    v1 = p2 - p1
    v2 = p0 - p2
    v3 = p2 - p0
    plane = np.cross(v0, v3)

    # minimun and maximun coordinates of the triangle
    for i in range(3):
        trix.append(triangle[i][0])
        triy.append(triangle[i][1])
        triz.append(triangle[i][2])
    minx, maxx = int(np.floor(np.min(trix))), int(np.ceil(np.max(trix)))
    miny, maxy = int(np.floor(np.min(triy))), int(np.ceil(np.max(triy)))
    minz, maxz = int(np.floor(np.min(triz))), int(np.ceil(np.max(triz)))

    # safe the points that are inside triangle
    points = []

    # go through each point in the box of minimum and maximum x,y,z
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            for z in range(minz, maxz + 1):

                # check the diagnals of each voxel cube if they are inside triangle
                if LinePlaneCollision(triangle, plane, p0, [1, 1, 1], [x - 0.5, y - 0.5, z - 0.5], [x, y, z]):
                    points.append([x, y, z])
                elif LinePlaneCollision(triangle, plane, p0, [-1, -1, 1], [x + 0.5, y + 0.5, z - 0.5], [x, y, z]):
                    points.append([x, y, z])
                elif LinePlaneCollision(triangle, plane, p0, [-1, 1, 1], [x + 0.5, y - 0.5, z - 0.5], [x, y, z]):
                    points.append([x, y, z])
                elif LinePlaneCollision(triangle, plane, p0, [1, -1, 1], [x - 0.5, y + 0.5, z - 0.5], [x, y, z]):
                    points.append([x, y, z])

                # check edge cases and if the triangle is completly inside the box
                elif intersect(triangle, [x, y, z], v0, p0):
                    points.append([x, y, z])
                elif intersect(triangle, [x, y, z], v1, p1):
                    points.append([x, y, z])
                elif intersect(triangle, [x, y, z], v2, p2):
                    points.append([x, y, z])

    # return the points that are inside the triangle
    return (points)


# check if the point is on the triangle border
def intersect(triangle, point, vector, origin):
    x, y, z = point[0], point[1], point[2]
    origin = np.array(origin)

    # check the x faces of the voxel point
    for xcube in range(x, x + 2):
        xcube -= 0.5
        if LinePlaneCollision(triangle, [1, 0, 0], [xcube, y, z], vector, origin, [x, y, z]):
            return (True)

    # same for y and z
    for ycube in range(y, y + 2):
        ycube -= 0.5
        if LinePlaneCollision(triangle, [0, 1, 0], [x, ycube, z], vector, origin, [x, y, z]):
            return (True)
    for zcube in range(z, z + 2):
        zcube -= 0.5
        if LinePlaneCollision(triangle, [0, 0, 1], [x, y, zcube], vector, origin, [x, y, z]):
            return (True)

    # check if the point is inside the triangle (in case the whole tri is in the voxel point)
    if origin[0] <= x + 0.5 and origin[0] >= x - 0.5:
        if origin[1] <= y + 0.5 and origin[1] >= y - 0.5:
            if origin[2] <= z + 0.5 and origin[2] >= z - 0.5:
                return (True)

    return (False)


# I modified this file to suit my needs:
# https://gist.github.com/TimSC/8c25ca941d614bf48ebba6b473747d72
# check if the cube diagnals cross the triangle in the cube
def LinePlaneCollision(triangle, planeNormal, planePoint, rayDirection, rayPoint, point, epsilon=1e-6):
    planeNormal = np.array(planeNormal)
    planePoint = np.array(planePoint)
    rayDirection = np.array(rayDirection)
    rayPoint = np.array(rayPoint)

    ndotu = planeNormal.dot(rayDirection)
    if abs(ndotu) < epsilon:
        return (False)

    w = rayPoint - planePoint
    si = -planeNormal.dot(w) / ndotu
    Psi = w + si * rayDirection + planePoint

    # check if they cross inside the voxel cube
    if np.abs(Psi[0] - point[0]) <= 0.5 and np.abs(Psi[1] - point[1]) <= 0.5 and np.abs(Psi[2] - point[2]) <= 0.5:
        # check if the point is inside the triangle and not only on the plane
        if PointInTriangle(Psi, triangle):
            return (True)
    return (False)


# I used the following file for the next 2 functions, I converted them to python. Read the article. It explains everything way better than I can.
# https://blackpawn.com/texts/pointinpoly#:~:text=A%20common%20way%20to%20check,triangle%2C%20otherwise%20it%20is%20not.
# check if point is inside triangle
def SameSide(p1, p2, a, b):
    cp1 = np.cross(b - a, p1 - a)
    cp2 = np.cross(b - a, p2 - a)
    if np.dot(cp1, cp2) >= 0:
        return (True)
    return (False)


def PointInTriangle(p, triangle):
    a = triangle[0]
    b = triangle[1]
    c = triangle[2]
    if SameSide(p, a, b, c) and SameSide(p, b, a, c) and SameSide(p, c, a, b):
        return (True)
    return (False)


your_mesh = mesh.Mesh.from_file('part2.stl')  # the stl file you want to voxelize

## set the height of your mesh
first = len(your_mesh.vectors)
for i in range(first):
    second = len(your_mesh.vectors[i])
    for j in range(second):
        third = len(your_mesh.vectors[i][j])
        for k in range(third):
            your_mesh.vectors[i][j][k] *= 0.1 # points per millimeter

            # print(first * i + second * j + third * k)

##
my_mesh = your_mesh.vectors.copy()  # shorten the name

voxel = []
temp = 0
deleteMe = len(my_mesh)
print(deleteMe)
t0 = time.time()

for i in range(len(my_mesh)):  # go though each triangle and voxelize it
    t1 = time.time()
    new_voxel = triangle_voxalize(my_mesh[i])
    voxel.append(new_voxel)
    t2=time.time()
    temp +=1
    print(str(temp) +'  current: ' + str(t2-t1) + '   running avg: ' + str(int((t2-t0)/temp)) + '   total time: ' + str(int(t2-t0)))




##
#print(len(voxel))  # number of points in the voxel

max_x = -math.inf
min_x = math.inf
max_y = -math.inf
min_y = math.inf
max_z = -math.inf
min_z = math.inf

for step in range(len(voxel)):
    for piece in voxel[step]:

        if piece[0] > max_x:
            max_x = piece[0]
        if piece[0] < min_x:
            min_x = piece[0]

        if piece[1] > max_y:
            max_y = piece[1]
        if piece[1] < min_y:
            min_y = piece[1]

        if piece[2] > max_z:
            max_z = piece[2]
        if piece[2] < min_z:
            min_z = piece[2]

len_x = max_x - min_x
len_y = max_y - min_y
len_z = max_z - min_z

# dim = max([len_x, len_y, len_z])

block = (np.zeros((len_x+1, len_y+1, len_z+1)))
for step in range(len(voxel)):
    for inc in voxel[step]:
        small_arr = list(inc)
        x = small_arr[0] - min_x
        y = small_arr[1] - min_y
        z = small_arr[2] - min_z
        block[x][y][z] = 1

SAVEasBINVOX(block)
MakeAPicture(block)

# split in x,y,z points
x_points = []
y_points = []
z_points = []
for x in range(len(voxel)):
    for y in range(len(voxel[x])):
        x_points.append(voxel[x][y][0])
        y_points.append(voxel[x][y][1])
        z_points.append(voxel[x][y][2])

## plot the voxel
ax = plt.axes(projection="3d")
ax.scatter3D(x_points, y_points, z_points)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

## plot 1 layer of the voxel
#for a in range(len(z_points)):
#    if z_points[a] == 300:
#        plt.scatter(x_points[a], y_points[a])

plt.show()

"""import numpy as np
from madcad.hashing import PositionMap
from madcad.io import read
import binvox_rw

def SAVEasBINVOX(block, dim):
    newfile = open('NEW.binvox', 'wb')
    block = block.tolist()
    for x in range(dim):
        for y in range(dim):
           for z in range(dim):
                if block[x][y][z] == 1:
                    block[x][y][z] = True
                else:
                    block[x][y][z] = False

    dims = [dim, dim, dim]
    translate = 0
    scale = 10
    axis_order = 'xyz'
    m2 = binvox_rw.Voxels(block, dims, translate, scale, axis_order)
    m2.write(newfile)



# load the obj file in a madcad Mesh
mymesh = read('part1.stl')
# choose the cell size of the voxel
size = 1

voxel = set()    # this is a sparse voxel
hasher = PositionMap(size)   # ugly object creation, just to use one of its methods
for face in mymesh.faces:
    voxel.update(hasher.keysfor(mymesh.facepoints(face)))

print(len(voxel))

tot_arr = list(voxel)
maxp = max(tot_arr)
dim = 0
for x in tot_arr:
    small_arr = list(x)
    for y in range(3):
        slice = small_arr[y]
        if slice > dim:
            dim = small_arr[y]


block = (np.zeros((dim*2, dim*2, dim*2)))

for inc in tot_arr:
    small_arr = list(inc)
    x=small_arr[0] + dim -1
    y=small_arr[1] + dim -1
    z=small_arr[2] + dim -1
    block[x][y][z] = 1

SAVEasBINVOX(block, dim*2)

"""
