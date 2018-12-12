#!/usr/bin/python3


import numpy as np
import sys
import math



InFileName = sys.argv[1] #get filename with ODF table from first argument of comand string
fon1 = np.genfromtxt(InFileName,skip_header = 150, skip_footer=1) 
fon2 = np.genfromtxt(InFileName,skip_header = 151, )
#print(fon1[:]) #debag output
#print(fon2[:]) #debag output
fon = np.hstack((fon1,fon2))
#print(fon) #debag output

#_______coefficient of defocusing

#defoc39 = np.array([1.00, 1.00, 1.01, 1.03, 1.05, 1.08, 1.12, 1.19, 1.31, 1.47, 1.66, 1.86, 2.08, 2.40, 2.95, 3.57, 5.62, 39,5])
#defoc48 = np.array([1.00, 1.00, 1.00, 1.01, 1.01, 1.03, 1.05, 1.09, 1.14, 1.22, 1.33, 1.48, 1.65, 1.90, 2.35, 2.90, 4.50, 48,3])
#defoc53 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03, 1.05, 1.12, 1.20, 1.32, 1.49, 1.71, 2.11, 2.71, 3.26, 52.8])
#defoc55 = np.array([1.00, 1.00, 1.00, 1.00, 1.01, 1.01, 1.03, 1.05, 1.09, 1.14, 1.23, 1.35, 1.50, 1.67, 1,83, 2,06, 2.42, 55.5])
#defoc68 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.03, 1.06, 1.11, 1.28, 1.29, 1.42, 1.58, 1.73, 1.94, 2.35, 67.9])
#defoc75 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.04, 1.08, 1.15, 1.24, 1.36, 1.50, 1.63, 1.83, 2.29, 75.0])
#defoc90 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.01, 1.02, 1.03, 1.03, 1.05, 1.07, 1.10, 1.22, 1.43, 1.72, 2.20, 90.3])
#defoc106 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03, 1.05, 1.10, 1.16, 1.24, 1.34, 1.44, 1.61, 2.12, 105.8])
#defoc115 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.04, 1.08, 1.13, 1.19, 1.27, 1.34, 1.50, 2.05, 114.7])
#defoc153 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.01, 1.03, 1.05, 1.09, 1.14, 1.19, 1.24, 1.39, 1.80, 153.4])

two_theta = float(sys.argv[2])


if two_theta < 39.5 : 
   defoc1 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.00])
   defoc2 = np.array([1.00, 1.00, 1.00, 1.01, 1.01, 1.03, 1.05, 1.09, 1.14, 1.22, 1.33, 1.48, 1.65, 1.90, 2.35, 2.90, 4.50, 48,3])
   two_theta_left = 0
   two_theta_right = 39.5
elif two_theta < 48.3 :
    defoc1 = np.array([1.00, 1.00, 1.01, 1.03, 1.05, 1.08, 1.12, 1.19, 1.31, 1.47, 1.66, 1.86, 2.08, 2.40, 2.95, 3.57, 5.62, 39,5])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.01, 1.01, 1.03, 1.05, 1.09, 1.14, 1.22, 1.33, 1.48, 1.65, 1.90, 2.35, 2.90, 4.50, 48,3])
    two_theta_left = 39.5
    two_theta_right = 48.3

elif two_theta < 52.8 : 
    defoc1 = np.array([1.00, 1.00, 1.00, 1.01, 1.01, 1.03, 1.05, 1.09, 1.14, 1.22, 1.33, 1.48, 1.65, 1.90, 2.35, 2.90, 4.50, 48,3])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03, 1.05, 1.12, 1.20, 1.32, 1.49, 1.71, 2.11, 2.71, 3.26, 52.8])
    two_theta_left = 48.3
    two_theta_right = 52.8

elif two_theta < 67.9 :
    defoc1 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03, 1.05, 1.12, 1.20, 1.32, 1.49, 1.71, 2.11, 2.71, 3.26, 52.8])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.03, 1.06, 1.11, 1.28, 1.29, 1.42, 1.58, 1.73, 1.94, 2.35, 67.9]) 
    two_theta_left = 52.8
    two_theta_right = 67.9

elif two_theta < 75.0 :
    defoc1 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.03, 1.06, 1.11, 1.28, 1.29, 1.42, 1.58, 1.73, 1.94, 2.35, 67.9])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.04, 1.08, 1.15, 1.24, 1.36, 1.50, 1.63, 1.83, 2.29, 75.0])
    two_theta_left = 67.9
    two_theta_right = 75.0

elif two_theta < 90.3 :
    defoc1 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.04, 1.08, 1.15, 1.24, 1.36, 1.50, 1.63, 1.83, 2.29, 75.0])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.01, 1.02, 1.03, 1.03, 1.05, 1.07, 1.10, 1.22, 1.43, 1.72, 2.20, 90.3])
    two_theta_left = 75.0
    two_theta_right = 90.3

elif two_theta < 105.8 :
    defoc1 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.01, 1.02, 1.03, 1.03, 1.05, 1.07, 1.10, 1.22, 1.43, 1.72, 2.20, 90.3])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03, 1.05, 1.10, 1.16, 1.24, 1.34, 1.44, 1.61, 2.12, 105.8])
    two_theta_left = 90.3
    two_theta_right = 105.8

elif two_theta < 114.7 :
    defoc1 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03, 1.05, 1.10, 1.16, 1.24, 1.34, 1.44, 1.61, 2.12, 105.8])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.04, 1.08, 1.13, 1.19, 1.27, 1.34, 1.50, 2.05, 114.7])
    two_theta_left = 105.8
    two_theta_right = 114.7

elif two_theta < 153.4 :
    defoc1 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.04, 1.08, 1.13, 1.19, 1.27, 1.34, 1.50, 2.05, 114.7])
    defoc2 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.01, 1.03, 1.05, 1.09, 1.14, 1.19, 1.24, 1.39, 1.80, 153.4])
    two_theta_left = 114.7
    two_theta_right = 153.4


OutFile=open(sys.argv[1]+'_new','w')
OutFile.write('1 header \n')
#OutFile.write('rot \t azimut \t intens \t backgr \t defoc \n')
OutFile.write('rot \t azimut \t intens \n')
intens = np.genfromtxt(InFileName,skip_header = 8, max_rows = 1)
m_intens =(intens[0]+intens[1]+ intens[2]+intens[3])/4
OutFile.write('0 \t 0 \t'+str((m_intens-fon[0])*1.00)+'\n')
skip_line = 10
for i in range(5,71,5):
    intens = []
    defoc = (two_theta-two_theta_left)*(defoc2[int(i/5)]-defoc1[int(i/5)])/(two_theta_right-two_theta_left)+defoc1[int(i/5)]
    for p in range(9):
        intens_1 = np.genfromtxt(InFileName,skip_header = skip_line, max_rows = 1)
        intens = np.hstack((intens,intens_1))
        skip_line = skip_line + 1
    #print(intens) #debag output
    for q in enumerate(intens):
        fon_numb = int(i/5)
        #OutFile.write(str(q[0]*5)+'\t'+str(i)+'\t'+str(intens[q[0]])+'\t'+str(fon[fon_numb])+'\t'+ str(defoc)+'\t'+'\n')
        OutFile.write(str(q[0]*5)+'\t'+str(i)+'\t'+str((intens[q[0]]-fon[fon_numb])*defoc)+'\n')
    skip_line = skip_line + 1
#for q in enumerate(X):
   # rot = math.atan2(Y[q[0]],X[q[0]])/math.pi*180
  #  azimute = math.fabs(angle[q[0]])
 #   OutFile.write(str(rot) + '\t' +str(azimute)+ '\t' +str(PP[q[0]])+'\n')
OutFile.close()




