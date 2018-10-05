#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt


path = "s_xy/postProc"
filename = "/256grains16x16x16_sxy_inc"
#iteration = 385
#step = 5

sigmaM = []
epsilonM = []
sigmaX = []
epsilonX = []
xlineM = []

for i in range(0, 250, 2):
    if(i < 10):
        fname = path+filename+"00"+str(i)+".txt"
    elif(i < 100):
        fname = path+filename+"0"+str(i)+".txt"
    else:
        fname = path+filename+str(i)+".txt"
    data = np.genfromtxt(fname, skip_header=7, usecols=(47, 48, 31, 40))
    stressM = data[:1001, 0]
    strainM = data[:1001, 1]
#modification for X-tension
    stressX = data[:1001, 2]
    strainX = data[:1001, 3]

    sigmaM.append(stressM.mean())
    epsilonM.append(strainM.mean())
    sigmaX.append(stressX.mean())
    epsilonX.append(strainX.mean())

#for i in range (0, len(sigmaM)):
#   print(sigmaM[i], sigmaX[i])

#Looking for sigma 0.2

tgaM = (sigmaM[2]-sigmaM[0])/(epsilonM[2]-epsilonM[0])
print(tgaM) 
for i in range (0, len(epsilonM)-1):
	y1M = tgaM*epsilonM[i] - tgaM*0.002
	y2M = tgaM*epsilonM[i+1] - tgaM*0.002
	if (sigmaM[i] > y1M) and (sigmaM[i+1] < y2M):
		s02M = (sigmaM[i]+sigmaM[i+1])/2
		xlineM.append(0.002)
		xlineM.append((epsilonM[i]+epsilonM[i+1])/2)
		print("Sigma0.2 (Mises) = ",s02M)
s02M_line = [0,s02M]

tgaX = (sigmaX[2]-sigmaX[0])/(epsilonX[2]-epsilonX[0])
print(tgaX) 
for i in range (0, len(epsilonX)-1):
	y1X = tgaX*epsilonX[i] - tgaX*0.002
	y2X = tgaX*epsilonX[i+1] - tgaX*0.002
	if (sigmaX[i] > y1X) and (sigmaX[i+1] < y2X):
		s02X = (sigmaX[i]+sigmaX[i+1])/2
		print("Sigma0.2 (along X) = ",s02X)
plotting
plt.plot(epsilonM, sigmaM, '.r', label='Mises')
plt.plot(xlineM,s02M_line, '-og')
plt.plot(epsilonX, sigmaX, '.b', label='X-axis')
plt.xlabel('Strain, mm/mm')
plt.ylabel('Stress, Pa')
plt.legend(bbox_to_anchor=(1,1), bbox_transform=plt.gcf().transFigure)
plt.show()
