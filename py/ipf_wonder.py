import os
import math
import numpy as np
#from itertools import combinations_with_replacement

#t=[]
#for hkl in combinations_with_replacement([-1,1,-2,2], 3):
#    t.append(hkl)
#print(t[1])
hkl1 = np.array([ [1, 1, 2], [-1, 1, 2], [1, -1, 2], [1, 1, -2], [-1, -1, 2], [-1, 1, -2],
                [1, -1, -2], [-1, -1, -2], [1, 2, 1], [-1, 2, 1], [1, -2, 1], [1, 2, -1],
                [-1, -2, 1], [-1, 2, -1], [1, -2, -1], [-1, -2, -1], [2, 1, 1], [-2, 1, 1],
                [2, -1, 1], [2, 1, -1], [-2, -1, 1], [-2, 1, -1], [2, -1, -1], [-2, -1, -1] ])
print(hkl1)
"""
psi = [math.radians(i*5) for i in range(0,12)] # or theta
phi = [math.radians(i*5) for i in range(0,10)] # or phi
#for K in range(0,len(psi)):
#    print(math.degrees(psi[K]))
#for K in range(0,len(phi)):
#    print(math.degrees(phi[K]))
x=[]
y=[]
z=[]
#print(math.degrees(psi[-1]),'\n',phi)
for N in range(len(psi)):
    for M in range(len(phi)):
        #x.append(math.tan(psi[N]/2)*math.cos(phi[M]))
        #y.append(math.tan(psi[N]/2)*math.sin(phi[M]))
        x.append(math.sin(psi[N])*math.cos(phi[M]))
        y.append(math.sin(psi[N])*math.sin(phi[M]))
        z.append(math.cos(psi[N]))
print(x[-1],y[-1],z[-1])
x011=math.sin(math.radians(45))*math.cos(math.radians(90))
y011=math.sin(math.radians(45))*math.sin(math.radians(90))
z011=math.cos(math.radians(45))
x111=math.sin(math.radians(54.74))*math.cos(math.radians(315))
y111=math.sin(math.radians(54.74))*math.sin(math.radians(315))
z111=math.cos(math.radians(54.74))
print(x011,y011,z011,'\n',x111,y111,z111)
#helper1=math.sqrt(math.pow(x[-1],2)+math.pow(y[-1],2)+math.pow(z[-1],2))
sq011=math.sqrt(math.pow(x011,2)+math.pow(y011,2)+math.pow(z011,2))
sq111=math.sqrt(math.pow(x111,2)+math.pow(y111,2)+math.pow(z111,2))
m=[]
for K in range (len(x)):
    sq=math.sqrt(math.pow(x[K],2)+math.pow(y[K],2)+math.pow(z[K],2))
    m1=(x[K]*x011+y[K]*y011+z[K]*z011)/(sq*sq011)
    m2=(x[K]*x111+y[K]*y111+z[K]*z111)/(sq*sq111)
    sch=m1*m2
    m.append(sch)

#print(len(m),len(x),len(z))
path2 = "d:\\"
os.chdir( path2 )
newfile = "hey.dat"
f = open(newfile, 'w')
k = 0
for i in range(len(x)):
    f.write(str('%3f' % x[i]) + "    " + str('%3f' % y[i]) +"    " +  str('%3f' % z[i]) + "    " +  str('%3f' % m[i]) +"\n")
f.close()"""
#dontgo = input("Нажмите Enter, чтобы закрыть программу")
