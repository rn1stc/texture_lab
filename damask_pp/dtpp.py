#!/usr/bin/env python3
#############################################################
# version = 2020-03-20   (YYYY-MM-DD)
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
    # converts quaternion to Euler angles of Bunge notation
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


def QNormalize(q):
    sq_norm = math.sqrt(q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2)
    q_normalized = np.array([q[0] / sq_norm, q[1] / sq_norm, q[2] / sq_norm, q[3] / sq_norm], dtype=float)
    return q_normalized

def quatWAvgMarkley(Q, weights):
    '''
    Averaging Quaternions.

    Arguments:
        Q(ndarray): an Mx4 ndarray of quaternions.
        weights(list): an M elements list, a weight for each quaternion.
    '''

    # Form the symmetric accumulator matrix
    A = np.zeros((4, 4))
    M = Q.shape[0]
    wSum = 0

    for i in range(M):
        q = Q[i, :]
        w_i = weights[i]
        A += w_i * (np.outer(q, q)) # rank 1 update
        wSum += w_i

    # scale
    A /= wSum

    # Get the eigenvector corresponding to largest eigen value
    return np.linalg.eigh(A)[1][:, -1]



needed_res = ['pos', 'orientation', 'elem']  # variables to extract from results
res_ind = list()
res_names = list()
## SWITCHES
texture_filter = False
texture_value = 1

phase_split = True
grain_avg = True

##

if texture_filter or grain_avg:
    needed_res.append('texture')

if phase_split:
    needed_res.append('phase')

lst = os.listdir('.')
lst.sort()
#print(lst)

for directory in ['ebsd', 'mat_conf']:
    if os.path.isdir(directory):
        shutil.rmtree(directory, ignore_errors=True)   # clear previous output
    os.makedirs(directory)

for filename in lst:     # loop over result files
    if filename.endswith('.txt') and not filename.endswith('nodal.txt'):
        with open(filename, 'rt') as f:
            headersize = int(f.readline()[0])
            for i in range(1, headersize):
                next(f)
            reader = csv.reader(f, delimiter='	', skipinitialspace=True)
            lineData = list()

            cols = next(reader)   # list of variables in results
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
                exec(needed_res[i] + ' = np.ndarray(shape=(' + str(res_matrix[i]) + ',), dtype=float)') # create array for result
            for line in reader:
                for i in range(len(needed_res)):
                    data_line = np.ndarray(shape=(res_matrix[i],), dtype=float)
                    for j in range(res_matrix[i]):
                        vector_var = ['totalvolfrac_twin', 'texture', 'elem', 'phase']
                        if any(needed_res[i] in s for s in vector_var):
                            data_line[j] = float(line[cols.index(needed_res[i])])   # for vector results
                        else:
                            data_line[j] = float(line[cols.index(str(j+1) + '_' + needed_res[i])])  # for matrix results
                    exec(needed_res[i] + ' = np.vstack([' + needed_res[i] + ', data_line])')

            for i in range(len(needed_res)):
                exec(needed_res[i] + ' = np.delete(' + needed_res[i] + ', (0), axis=0)')  # deletes first empty line in array
            rotation_angles = np.array([0], dtype=float)
            if filename.endswith('inc0000.txt'):
                orientation0 = orientation   # stores initial orientations

            orintation_twd = np.ndarray(shape=(4,), dtype=float)
            twinned_grain_count = np.zeros((18,), dtype=int)
            # orientation = orientation0   # uncomment to show only twinning

            geom_dim = round(len(pos[:, 0]) ** (1 / 3))

            ## Not twinned euler angles output
            filename3 = 'ebsd/' + filename[:-4] + '.ebsd'
            f3 = open(filename3, 'w')
            f3.write("x   y   z   phi1   PHI   phi2\n")
            if not texture_filter:
                for i in range(0, len(pos[:, 0])):
                    eulerangles = QToEuler(orientation[i, :]) * 57.2958
                    f3.write("%6.2f   %6.2f   %6.2f   %6.2f   %6.2f   %6.2f\n" % (
                        pos[i, 0], pos[i, 1], pos[i, 2], eulerangles[0], eulerangles[1], eulerangles[2]))
            else:
                for i in range(0, len(pos[:, 0])):
                    if texture[i] == texture_value:
                        eulerangles = QToEuler(orientation[i, :]) * 57.2958
                        f3.write("%6.2f   %6.2f   %6.2f   %6.2f   %6.2f   %6.2f\n" % (
                             pos[i, 0], pos[i, 1], pos[i, 2], eulerangles[0], eulerangles[1], eulerangles[2]))
            f3.close()

            ## Normal quaternion output
            filename_tw_q = 'ebsd/' + filename[:-4] + '.q'
            f_tw_q = open(filename_tw_q, 'w')
            f_tw_q.write("   x        y        z      Quat real    Quat i      Quat j      Quat k\n")
            if not texture_filter:
                for i in range(0, len(pos[:, 0])):
                    f_tw_q.write("%6.2f   %6.2f   %6.2f   %9.5f   %9.5f   %9.5f   %9.5f\n" % (
                        pos[i, 0], pos[i, 1], pos[i, 2], orientation[i, 0], orientation[i, 1],
                        orientation[i, 2], orientation[i, 3]))
            else:
                for i in range(0, len(pos[:, 0])):
                    if texture[i] == texture_value:
                        f_tw_q.write("%6.2f   %6.2f   %6.2f   %9.5f   %9.5f   %9.5f   %9.5f\n" % (
                            pos[i, 0], pos[i, 1], pos[i, 2], orientation[i, 0], orientation[i, 1],
                            orientation[i, 2], orientation[i, 3]))
            f_tw_q.close()

            if phase_split and int(max(phase) + 1) > 1:
                for phase_id in range(1, int(max(phase) + 1)):
                    filename_q_ph = 'ebsd/phase_' + str(phase_id) + '_' + filename[:-4] + '.q'
                    f_q_ph = open(filename_q_ph, 'w')
                    f_q_ph.write("   x        y        z      Quat real    Quat i      Quat j      Quat k\n")
                    for i in range(0, len(pos[:, 0])):
                        if phase[i] == phase_id:
                            f_q_ph.write("%6.2f   %6.2f   %6.2f   %9.5f   %9.5f   %9.5f   %9.5f\n" % (
                                pos[i, 0], pos[i, 1], pos[i, 2], orientation[i, 0], orientation[i, 1],
                                orientation[i, 2], orientation[i, 3]))
                    f_q_ph.close()

            if grain_avg:
                if max(texture) > 200:
                    continue
                if phase is None:
                    phase = np.ones((len(pos[:, 0]),), dtype=int)
                for phase_id in range(1, int(max(phase) + 1)):
                    filename_q_ph = 'ebsd/grain_avg_phase_' + str(phase_id) + '_' + filename[:-4] + '.q'
                    f_q_ph = open(filename_q_ph, 'w')
                    f_q_ph.write("   x        y        z      Quat real    Quat i      Quat j      Quat k\n")
                    for texture_id in range(1, int(max(texture) + 1)):
                        quats = np.ndarray(shape=(4,), dtype=float)
                        for i in range(0, len(pos[:, 0])):
                            if phase[i] == phase_id and texture[i] == texture_id:
                                quats = np.vstack([quats, orientation[i, :]])
                        quats = np.delete(quats, (0), axis=0)
                        try:
                            quats[:, 0].shape[0]
                        except IndexError:
                            continue
                        lines = quats[:, 0].shape[0]
                        q_avg = quatWAvgMarkley(quats, np.ones(lines))
                        f_q_ph.write("%6.2f   %6.2f   %6.2f   %9.5f   %9.5f   %9.5f   %9.5f\n" % (
                            pos[i, 0], pos[i, 1], pos[i, 2], q_avg[0], q_avg[1],q_avg[2], q_avg[3]))
                    f_q_ph.close()



            ## Material.config output for DAMASK simulation restart
            filename_mc = 'mat_conf/' + filename[:-4] + '.material.config'
            f_mc = open(filename_mc, 'w')
            f_mc.write("# Orientations from DAMASK output file %s\n" % filename[:-4])
            f_mc.write("#-------------------#\n<microstructure>\n#-------------------#\n")
            for i in range(0, len(pos[:, 0])):
                f_mc.write("[Grain%05d]\ncrystallite 1\n" % (elem[i]))
                f_mc.write("(constituent)   phase %d   texture    %d   fraction 1.0\n" %
                           ((phase[i] if phase_split else 1),  elem[i]))
            f_mc.write("#-------------------#\n<texture>\n#-------------------#\n")
            for i in range(0, len(pos[:, 0])):
                euler = QToEuler(orientation[i, :]) * 57.2958
                if euler[2] < 0: euler[2] = euler[2] + 360
                f_mc.write("[Grain%05d]\n" % (elem[i]))
                f_mc.write("(gauss)	phi1 %6.2f	Phi %6.2f	phi2 %6.2f	scatter 0.0	fraction 1.0\n" % (
                    euler[0], euler[1], euler[2]))

            f_mc.close()

## Geometry output for DAMASK simulation restart
filename_geom = 'mat_conf/continue.geom'
f_geom = open(filename_geom, 'w')
f_geom.write("6	header\ngeom_from_twin_rotate\ngrid	a %d	b %d	c %d\nsize	x 1.0	y 1.0	z 1.0\n" % (geom_dim, geom_dim, geom_dim) +
             "origin	x 0.0	y 0.0	z 0.0\nhomogenization	1\nmicrostructures	%d\n" % (geom_dim ** 3))
for i in range(0, geom_dim ** 2):
    for j in range(0, geom_dim):
        f_geom.write("%4d " % (i * geom_dim + j + 1))
    f_geom.write("\n")
f_geom.close()