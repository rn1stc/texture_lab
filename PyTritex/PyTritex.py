#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
#########################################################################


vectors = np.array([[1,0,0],
                    [1,1,0],
                    [0,0,1],
                    [2,0,1],
                    [1,1,1],
                    [1,0,5],
                    [2,1,1]])
system = 'hex'                        # cubic or hex
a = 3.23                                 # lattice constant
c = 5.14                               # lattice constant, any if not applicable


#########################################################################
# ver = 2018-oct-05
if system == 'cubic':
    G = np.array([[a**2,    0,        0],
                  [0,        a**2,    0],
                  [0,        0,       a**2]])

elif system == 'hex':
    G = np.array([[a ** 2, 0, 0],
                  [0, a ** 2, 0],
                  [0, 0, c ** 2]])
    # G = np.array([[a**2,      -.5*a**2,   0],
    #               [-.5*a**2,  a**2,       0],
    #               [ 0,        0,          c**2]])

vec = np.empty(shape=[0, 3])
vec = np.vstack([vec, vectors])
vec1 = np.empty(shape=[0, 3])
points_yz = np.empty(shape=[0, 2])
x_dir = np.array([1, 0, 0])
y_dir = np.array([0, 1, 0])
z_dir = np.array([0, 0, 1])
def projectdir(a, b, c):
    if system == 'hex':
        a = (2 * a + b) / 0.866
        #b = (b ** 2 + (a + b) ** 2) ** 0.5
    vector = np.array([a, b, c])
    theta = np.arccos((z_dir @ G @ vector) / ((vector @ G @ vector) ** .5 * (z_dir @ G @ z_dir) ** .5))
    vec_proj = np.array([vector[0], vector[1], 0])
    if ((vector[0] == 0) and (vector[1] == 0)): phi = 0
    else:
        phi = np.arccos((x_dir @ G @ vec_proj) / ((vec_proj @ G @ vec_proj) ** .5 * (x_dir @ G @ x_dir) ** .5))
    if system == 'hex': phi = phi * 2
    x = abs(np.tan(theta / 2) * np.cos(phi))
    y = abs(np.tan(theta / 2) * np.sin(phi))
    return [x, y]

for i in range(len(vec[:,1])):
    points_yz = np.vstack([points_yz, projectdir(vec[i, 0], vec[i, 1], vec[i, 2])])
tri = np.array([0, 0])
if system == 'cubic':
    for z in np.arange(0., 1.01, 0.01):
        tri = np.vstack( [tri, projectdir(1, z, 1)])
elif system == 'hex':
    for z in np.arange(0., 1.01, 0.01):
        tri = np.vstack( [tri, projectdir(1, z, 0)])
tri = np.vstack([tri, tri[0,:]])

plt.figure(num=None, figsize=(6, 4), dpi=96, facecolor='w', edgecolor='k')
plt.plot(tri[:,0], tri[:,1],linewidth=3.0)
plt.plot(points_yz[:,0], points_yz[:,1], '*',linewidth=3.0, markersize=15)
plt.axis('equal')
plt.axis('off')

if system == 'cubic':
    plt.text(-.1, 0, '[001]', fontsize=15)
    plt.text(0.43, 0, '[101]', fontsize=15)
    plt.text(0.38, 0.37, '[111]', fontsize=15)

elif system == 'hex':
    plt.text(-.2, 0, '[0001]', fontsize=15)
    plt.text(1.03, 0, r'$[10\bar10]$', fontsize=15)
    plt.text(0.92, 0.53, r'$[11\bar20]$', fontsize=15)

plt.savefig('triangle.png')
plt.show()