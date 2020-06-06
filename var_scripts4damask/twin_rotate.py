#!/usr/bin/env python3
#############################################################
# version = 2018-11-12   (YYYY-MM-DD)
#
#
#############################################################

import csv, os, math, shutil
import numpy as np


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def QConj(q):
    q = np.append(q[0], -1 * q[1:4])
    return q


def QToEuler(q):
    q = QConj(q)
    res_euler = np.ndarray(shape=(3,), dtype=float)
    res_euler[1] = math.acos(1.0 - 2.0 * (q[1]**2 + q[2]**2))
    if abs(res_euler[1]) < 1e-6:
        res_euler[0] = math.copysign(2.0 * math.acos(clamp(q[0],-1, 1)), q[3])
        res_euler[2] = 0.0
    else:
        res_euler[0] = math.atan2(+q[0]*q[2]+q[1]*q[3], q[0]*q[1]-q[2]*q[3])
        res_euler[2] = math.atan2(-q[0]*q[2]+q[1]*q[3], q[0]*q[1]+q[2]*q[3])
    if res_euler[0] < 0: res_euler = res_euler + np.array([2*np.pi, 0, 0])
    return res_euler


def QMult(q, r):
    t0 = r[0] * q[0] - r[1] * q[1] - r[2] * q[2] - r[3] * q[3]
    t1 = r[0] * q[1] + r[1] * q[0] - r[2] * q[3] + r[3] * q[2]
    t2 = r[0] * q[2] + r[1] * q[3] + r[2] * q[0] - r[3] * q[1]
    t3 = r[0] * q[3] - r[1] * q[2] + r[2] * q[1] + r[3] * q[0]
    t = np.array([t0, t1, t2, t3], dtype=float)
    return t


def QNormalize(q):
    sq_norm = math.sqrt(q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2)
    q_normalized = np.array([q[0] / sq_norm, q[1] / sq_norm, q[2] / sq_norm, q[3] / sq_norm], dtype=float)
    return q_normalized


def MillerToEuler(ts):
    # 33 13 23 31 32 row-column
    a33 = ts[7] / math.sqrt(ts[4] ** 2 + ts[5] ** 2 + ts[7] ** 2)
    a23 = ts[5] / math.sqrt(ts[4] ** 2 + ts[5] ** 2 + ts[7] ** 2)
    a31 = ts[3] / math.sqrt(ts[0] ** 2 + ts[1] ** 2 + ts[3] ** 2)
    a13 = ts[4] / math.sqrt(ts[4] ** 2 + ts[5] ** 2 + ts[7] ** 2)
    a11 = ts[0] / math.sqrt(ts[0] ** 2 + ts[1] ** 2 + ts[3] ** 2)
    n = np.array([ts[0], ts[1], ts[3]])
    b = np.array([ts[4], ts[5], ts[7]])
    t = np.cross(n,b)
    a32 = t[2]
    a12 = t[0]
    if abs(a33 - 1.0) < 1e-2:
        PHI = 0
        phi1 = math.atan2(a12, a11) / 2
        phi2 = - phi1
    else:
        PHI = math.acos(a33)
        sinPHI = math.sin(PHI)
        phi2 = math.atan2(a13 / sinPHI, a23 / sinPHI)
        phi1 = math.atan2(a31 / sinPHI, a32 / sinPHI)
    return np.array([phi1, PHI, phi2])


def EulerToQ(eu):
    c = math.cos(0.5 * eu[1])
    s = math.sin(0.5 * eu[1])
    sigma = 0.5 * (eu[0] + eu[2])
    delta = 0.5 * (eu[0] - eu[2])
    q = np.array([c * math.cos(sigma), s * math.cos(delta), s * math.sin(delta), c * math.sin(sigma)])
    QConj(q)
    return q


needed_res = ['pos', 'eulerangles', 'orientation', 'accumulatedshear_twin']
res_ind = list()
res_names = list()

twin_ind = np.array([
# dir(uvw)           normal(?)(hkl)
[1, -1,  0,  1,    -1,  1,  0,  2, ], # <-10.1>{10.2} shear = (3-(c/a)^2)/(sqrt(3) c/a)
[1,  0,  1,  1,     1,  0, -1,  2, ],
[0,  1, -1,  1,     0, -1,  1,  2, ],
[1,  1,  0,  1,     1, -1,  0,  2, ],
[1,  0, -1,  1,    -1,  0,  1,  2, ],
[0, -1,  1,  1,     0,  1, -1,  2, ],
#
[2, -1, -1,  6,    -2,  1,  1,  1, ], # <11.6>{-1-1.1} shear = 1/(c/a)
[1,  2, -1,  6,     1, -2,  1,  1, ],
[1, -1,  2,  6,     1,  1, -2,  1, ],
[2,  1,  1,  6,     2, -1, -1,  1, ],
[1, -2,  1,  6,    -1,  2, -1,  1, ],
[1,  1, -2,  6,    -1, -1,  2,  1, ],
#
# [1,  1,  0, -2,    -1,  1,  0,  1, ], ## <10.-2>{10.1} shear = (4(c/a)^2-9)/(4 sqrt(3) c/a)
# [1,  0, -1, -2,     1,  0, -1,  1, ],
# [0, -1,  1, -2,     0, -1,  1,  1, ], # comment unused systems
# [1, -1,  0, -2,     1, -1,  0,  1, ],
# [1,  0,  1, -2,    -1,  0,  1,  1, ],
# [0,  1, -1, -2,     0,  1, -1,  1, ],
#
[2, -1, -1, -3,     2, -1, -1,  2, ],# <11.-3>{11.2} shear = 2((c/a)^2-2)/(3 c/a)
[1,  2, -1, -3,    -1,  2, -1,  2, ],
[1, -1,  2, -3,    -1, -1,  2,  2, ],
[2,  1,  1, -3,    -2,  1,  1,  2, ],
[1, -2,  1, -3,     1, -2,  1,  2, ],
[1,  1, -2, -3,     1,  1, -2,  2  ]
], np.int32)

twin_q = np.zeros(shape=(len(twin_ind[:,0]), 4), dtype=float)
for i in range(len(twin_ind[:,0])):
    twin_q[i,:] = EulerToQ(MillerToEuler(twin_ind[i,:]))

lst = os.listdir('.')
lst.sort()
#print(lst)

for directory in ['ebsd', 'twinned_ebsd']:
    if os.path.isdir(directory):
        shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory)

for filename in lst:
    if filename.endswith('.txt'):
        with open(filename, 'rt') as f:
            headersize = int(f.readline()[0])
            for i in range(1, headersize):
                next(f)
            reader = csv.reader(f, delimiter='	', skipinitialspace=True)
            lineData = list()

            cols = next(reader)
            #print(cols)

            for col in cols:

                lineData.append(list())
            res_matrix = list()
            for result in needed_res:
                res_matrix_ind = 0
                for col in cols:
                    if col.endswith(result):
                        res_ind.append(cols.index(col))
                        res_names.append(col)
                        res_matrix_ind = res_matrix_ind + 1
                res_matrix.append(res_matrix_ind)




            for i in range(len(needed_res)):
                exec(needed_res[i] + ' = np.ndarray(shape=(' + str(res_matrix[i]) + ',), dtype=float)')
            for line in reader:
                for i in range(len(needed_res)):
                    data_line = np.ndarray(shape=(res_matrix[i],), dtype=float)
                    for j in range(res_matrix[i]):
                        data_line[j] = float(line[cols.index(str(j+1) + '_' + needed_res[i])])
                    exec(needed_res[i] + ' = np.vstack([' + needed_res[i] + ', data_line])')
                # print(eulerangles[-1, :])
                # print(orientation[-1, :])
                # print(QToEuler(orientation[-1, :]) * 57.2958)
                # print('------------------------')
            for i in range(len(needed_res)):
                exec(needed_res[i] + ' = np.delete(' + needed_res[i] + ', (0), axis=0)')
            rotation_angles = np.array([0], dtype=float)

            orintation_twd = np.ndarray(shape=(4,), dtype=float)

            for i in range(len(orientation[:, 0])):
                twinned_ori = orientation[i, :]
                for j in range(len(accumulatedshear_twin[0, :])):
                    twin_sys_vec = np.array([0, twin_q[j, 1], twin_q[j, 2], twin_q[j, 3]])
                    # twin_sys_vec = np.array([0, twin_ind[j, 0], twin_ind[j, 1], twin_ind[j, 3]])
                    abs_tq = QMult(orientation[i, :], QMult(twin_sys_vec, QConj(orientation[i, :])))
                    abs_tq = QNormalize(abs_tq)
                    rot_angle = math.atan(accumulatedshear_twin[i, j])
                    rotation_angles = np.append(rotation_angles, abs(rot_angle * 57))
                    sin_rot_angle2 = math.sin(rot_angle / 2)
                    cos_rot_angle2 = math.cos(rot_angle / 2)
                    rot_q = np.array([cos_rot_angle2, abs_tq[1] * sin_rot_angle2, abs_tq[2] * sin_rot_angle2, abs_tq[3] * sin_rot_angle2])
                    rot_q = QNormalize(rot_q)

                    twinned_ori = QMult(twinned_ori, rot_q)

                orintation_twd = np.vstack([orintation_twd, twinned_ori])
            orintation_twd = np.delete(orintation_twd, (0), axis=0)
            print(filename, '  Avg. twin rotation = ', np.mean(rotation_angles), ' deg')




            filename2 = 'twinned_ebsd/' + filename[:-4] + '.ebsd'
            f2 = open(filename2, 'w')
            f2.write("x   y   z   phi1   PHI   phi2\n")
            twin_diff = np.array([0], dtype=float)
            euler_diff = np.ndarray(shape=(3,), dtype=float)
            for i in range(0,len(pos[:, 0])):
                twinned_euler = QToEuler(orintation_twd[i, :]) * 57.2958
                dif_vector = twinned_euler - eulerangles[i, :]
                if not any(abs(t) > 300 for t in dif_vector):
                    twin_diff = np.append(twin_diff, np.mean(abs(dif_vector)))
                    euler_diff = np.vstack([euler_diff, dif_vector])

                #if (not any(abs(t) > 300 for t in dif_vector)) and any(t > 10 for t in dif_vector):
                    #print(i, dif_vector)

                f2.write("%6.2f   %6.2f   %6.2f   %6.2f   %6.2f   %6.2f\n" % (pos[i,0], pos[i,1], pos[i,2], twinned_euler[0], twinned_euler[1], twinned_euler[2]))
            f2.close()
            print(filename, '  Euler difference = ', np.mean(twin_diff), ' deg')
            print(filename, '  Euler difference average by comp. = ', np.mean(euler_diff[:, 0]), ' deg ', np.mean(euler_diff[:, 1]), ' deg ', np.mean(euler_diff[:, 2]), ' deg ')

            filename3 = 'ebsd/' + filename[:-4] + '.ebsd'
            f3 = open(filename3, 'w')
            f3.write("x   y   z   phi1   PHI   phi2\n")
            for i in range(0, len(pos[:, 0])):
                f3.write("%6.2f   %6.2f   %6.2f   %6.2f   %6.2f   %6.2f\n" % (
                pos[i, 0], pos[i, 1], pos[i, 2], eulerangles[i, 0], eulerangles[i, 1], eulerangles[i, 2]))
            f3.close()