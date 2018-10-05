import numpy as np
from matplotlib import patches
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

#sx_r,sy_r,sz_r = 239469048, 249447594, 254311167 #random texture sigma02 values
#sx_t,sy_t,sz_t = 241541494, 252556780, 256652642 #tube4 texture sigma02 values

#recalc with more increments in elastic-plastic transition, sigma01
#STRESS TYPE: VON MISES EQUIVALENT
#sx_1,sy_1,sz_1 = 253621517, 253789791, 252806466 #random texture
#sx_2,sy_2,sz_2 = 237788322, 244039903, 246336156 #tube4 texture
#sx_3,sy_3,sz_3 = 244663166, 250818431, 256365826 #sharp def texture

#STRESS TYPE: CAUCHY TENSOR COMPONENT ALONG LOAD AXIS
sx_1,sy_1,sz_1 = 227381128, 235785345, 239707325 #random texture
sx_2,sy_2,sz_2 = 223260410, 231107341, 236791008 #tube4 texture 
sx_3,sy_3,sz_3 = 227603755, 238210788, 246877159 #sharp def texture 
#note: x is along RD, y - TD, z - ND

sx_1 = sx_1/np.power(10,6) #eliminate mega
sy_1 = sy_1/np.power(10,6)
sz_1 = sz_1/np.power(10,6)
sx_2 = sx_2/np.power(10,6)
sy_2 = sy_2/np.power(10,6)
sz_2 = sz_2/np.power(10,6)
sx_3 = sx_3/np.power(10,6)
sy_3 = sy_3/np.power(10,6)
sz_3 = sz_3/np.power(10,6)
#print('sx_1 = ',sx_1)

F1 = 0.5*(1/(sy_1*sy_1)+1/(sz_1*sz_1)-1/(sx_1*sx_1)) #coefficients
G1 = 0.5*(1/(sx_1*sx_1)+1/(sz_1*sz_1)-1/(sy_1*sy_1))
H1 = 0.5*(1/(sy_1*sy_1)+1/(sx_1*sx_1)-1/(sz_1*sz_1))
F2 = 0.5*(1/(sy_2*sy_2)+1/(sz_2*sz_2)-1/(sx_2*sx_2))
G2 = 0.5*(1/(sx_2*sx_2)+1/(sz_2*sz_2)-1/(sy_2*sy_2))
H2 = 0.5*(1/(sy_2*sy_2)+1/(sx_2*sx_2)-1/(sz_2*sz_2))
F3 = 0.5*(1/(sy_3*sy_3)+1/(sz_3*sz_3)-1/(sx_3*sx_3))
G3 = 0.5*(1/(sx_3*sx_3)+1/(sz_3*sz_3)-1/(sy_3*sy_3))
H3 = 0.5*(1/(sy_3*sy_3)+1/(sx_3*sx_3)-1/(sz_3*sz_3))
#print('coeff = ',Fr,Gr,Hr,Ft,Gt,Ht)

xcenter, ycenter = 0.0, 0.0
angle1 = -0.5*np.arctan((2*H1)/(F1-H1)) #tilt angle
angle2 = -0.5*np.arctan((2*H2)/(F2-H2))
angle3 = -0.5*np.arctan((2*H3)/(F3-H3)) 
print('angles = ', np.degrees(angle1),np.degrees(angle2),np.degrees(angle3))

#new formulation of coeff. 1/a^2, 1/b^2 ? (thesis Ohio)
#widthr = (Fr+Gr)/2-((Fr-Gr)/2*((1+np.sin(2*angler))/np.cos(2*angler)))
#x2 distance cut from axes 
width1 = (F1+G1+2*H1)/2-(F1-G1)/2*np.cos(2*angle1)+H1*np.sin(2*angle1)
height1 = (F1+G1+2*H1)/2-(F1-G1)/2*np.cos(2*angle1)-H1*np.sin(2*angle1)
width2 = (F2+G2+2*H2)/2-(F2-G2)/2*np.cos(2*angle2)+H2*np.sin(2*angle2)
height2 = (F2+G2+2*H2)/2-(F2-G2)/2*np.cos(2*angle2)-H2*np.sin(2*angle2)
width3 = (F3+G3+2*H3)/2-(F3-G3)/2*np.cos(2*angle3)+H3*np.sin(2*angle3)
height3 = (F3+G3+2*H3)/2-(F3-G3)/2*np.cos(2*angle3)-H3*np.sin(2*angle3)
width1 = 2/(np.power(width1,1/2))
height1 = 2/(np.power(height1,1/2))
width2 = 2/(np.power(width2,1/2))
height2 = 2/(np.power(height2,1/2))
width3 = 2/(np.power(width3,1/2))
height3 = 2/(np.power(height3,1/2))
print('Values, MPa = ',width1, height1, width2, height2, width3, height3)

theta = np.deg2rad(np.arange(0.0, 360.0, 1.0)) #grid (currently not used)
x = 0.5 * width1 * np.cos(theta)
y = 0.5 * height1 * np.sin(theta)
rtheta = np.radians(angle1) 
R = np.array([
    [np.cos(rtheta), -np.sin(rtheta)],
    [np.sin(rtheta),  np.cos(rtheta)],
    ])
x, y = np.dot(R, np.array([x, y]))
print(x,y)

#plotting (used)
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
for p in [
    patches.Ellipse(
        (xcenter, ycenter), width1, height1, angle=np.degrees(-angle1), fill=False,
        edgecolor=None      
    ),
    patches.Ellipse(
        (xcenter, ycenter), width2, height2, angle=np.degrees(-angle2), fill=False,
        edgecolor="red"     
    ),
    patches.Ellipse(
        (xcenter, ycenter), width3, height3, angle=np.degrees(-angle3), fill=False,
        edgecolor="green"     
    ),
]:
    ax.add_patch(p)

#makes axes in the center (somehow)
for direction in ["left","bottom"]:
    ax.spines[direction].set_position('zero')
    ax.spines[direction].set_smart_bounds(True)
for direction in ["right","top"]:
    ax.spines[direction].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True)

#customizing grid ticks and their labels; pain in the arse
plt.xlim([-350,350])
plt.ylim([-350,350])
major_ticks = np.arange(-350, 351, 50)
#minor_ticks = np.arange(-350, 351, 25)
ax.set_xticks(major_ticks)
ax.set_yticks(major_ticks)
#ax.set_xticks(minor_ticks, minor=True)
#ax.set_yticks(minor_ticks, minor=True)
#ax.grid(which='minor', alpha=0.2)
#ax.grid(which='major', alpha=0.5)

ax.set_xlabel(r'$\sigma_x$, MPa')
ax.set_ylabel(r'$\sigma_y$, MPa', rotation='horizontal')
ax.xaxis.set_label_coords(1.03, 0.5)
ax.yaxis.set_label_coords(0.5, 1.03)

dx = [sx_1,sx_2,sx_3]
dy = [sy_1,sy_2,sy_3]
plt.scatter(dx, [0,0,0])
plt.scatter([0,0,0], dy, alpha=0.5)

plt.show()
