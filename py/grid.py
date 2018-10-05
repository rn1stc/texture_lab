from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
import os
np.set_printoptions(threshold=np.nan)
# make up data.
#npts = int(raw_input('enter # of random points to plot:'))
seed(0)

#changing path to file
path = "d:\\texture\\srf\\"
os.chdir( path )
retval = os.getcwd()
print ("Смена директории: %s" % retval)
filename = input("Введите номер файла (без расширения) \n")
file = filename + ".dat"
#checking if file
while not os.path.exists(file):
    print ("Файл не найден. Попробуйте еще раз.")
    filename = input("Введите номер файла (без расширения)\n")
    file = filename + ".dat"
else:
    print ("Файл " + file + " обнаружен.\n")
#open file, read first line (because of f-paramters in the file)
f = open(file)
f.readline()
ar = np.fromfile(f, dtype=float, count=-1, sep=' ') #build an array from file
count = len(ar)/4
ar.shape = (int(count),4)
print(ar.shape) #just to be shure, shape of an array should be (1079,4): (x,y,z,tilt_angle)
npts = count
Numofcont = input("Введите число контуров \n")
#define data
x = ar[:,0]
y = ar[:,1]
z = ar[:,2]
# define grid.
xi = np.linspace(-0.81, 0.81, 100)
yi = np.linspace(-0.81, 0.81, 200)
# grid the data.
zi = griddata(x, y, z, xi, yi, interp='linear')
# contour the gridded data, plotting dots at the nonuniform data points.
CS = plt.contour(xi, yi, zi, int(Numofcont), linewidths=0.5, colors='k')
CS = plt.contourf(xi, yi, zi, int(Numofcont),
                  vmax=abs(zi).max(), vmin=0,cmap='inferno')
plt.colorbar()  # draw colorbar
# plot data points.
#plt.scatter(x, y, marker=',', s=1, zorder=10)
Max_x = np.amax(x) - 0.005
Max_xx = Max_x + 0.15
Max_xxx = Max_xx + 0.05
plt.xlim(-float(Max_xxx), float(Max_xxx))
plt.ylim(-float(Max_xxx), float(Max_xxx))
circle1 = plt.Circle((0, 0), float(Max_x), color='k', fill=False, linewidth=2)
circle2 = plt.Circle((0, 0), float(Max_xx), color='k', fill=False, linewidth=1.5)
plt.gcf().gca().add_artist(circle1)
plt.gcf().gca().add_artist(circle2)
plt.title('Pole figure for file ' + filename)
plt.show()
