#############################################################
# version = 2018-jun-15
#
#
#############################################################
import numpy as np
import os

odf_name = "11207.TXT"

f1 = open(odf_name, "r")
f2 = open('tmp.tmp', 'w')

for line in f1:
    count = 0
    tmp = line
    while count < 7:
        tmp = tmp.replace('  ', ' ')
        count += 1
    tmp = tmp.replace('E+', ' E +')
    tmp = tmp.replace('E-', ' E -')
    tmp = tmp.replace('ODF', 'ODF JUNK POWER')
    f2.write(tmp)
f1.close()
f2.close()
f2 = open('tmp.tmp', 'r')
data = []
data = np.genfromtxt(f2, dtype=[('f1','f8'), ('f2','f8'), ('f3','f8'), ('f4','f8'),('s5','S5'), ('f6','f8')], delimiter=" ", skip_header=1)
f2.close()
#np.sort(data, order='f3')
data = np.sort(data, order=['f1', 'f3'])
os.remove('tmp.tmp')
f2 = open(odf_name + '.linearODF', 'w')
f2.write("1 header\nphi1     Phi    phi2 intensity\n")
for line in data:
    for i in range(0, 3):
        if line[i] == 0:
            line[i] = line[i] + 0.5
    if line[0] == 360:
        line[0] = 359.5
    if line[1] == 60:
        line[1] = 59.5
    if line[2] == 90:
        line[2] = 89.5
    f2.write("%s   %s   %s   %s\n" % (line[0], line[2], line[1], line[3]*10**(line[5])))
f2.close()
