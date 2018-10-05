#############################################################
# version = 2018-jun-13
#
#
#############################################################

import csv, os, glob, shutil
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

if os.path.exists('avg_img'): shutil.rmtree('avg_img')
if os.path.exists('avg_txt'): shutil.rmtree('avg_txt')

list_avg = ['_eulerangles', '_f', '_p', '_resistance_slip', '_shearrate_slip','_resolvedstress_slip',
            '_resistance_twin', '_shearrate_twin', '_resolvedstress_twin', '_resistance', '_shearrate', '_resolvedstress']
dataavg = list()
dataabsavg = list()
lst = os.listdir('.')
lst.sort()
h = len(glob.glob1('.',"*.txt"))
for filename in lst:
    if filename.endswith('.txt'):
        with open(filename, 'rt') as f:
            headersize = int(f.readline()[0])
            for i in range(1, headersize):
                next(f)
            reader = csv.reader(f, delimiter='	', skipinitialspace=True)

            cols = next(reader)
            w = len(cols)
            print(cols)
            data = np.zeros(w, dtype=np.float32)
            dataabs = np.zeros(w, dtype=np.float32)
            i = 1

            for line in reader:
                data = data + np.asarray([float(k) if k != 'n/a' else 1 for k in line])
                dataabs = dataabs + np.asarray([abs(float(k)) if k != 'n/a' else 1 for k in line])
                i = i + 1

            data = data / ( i - 1 )
            dataavg.append(data)
            dataabs = dataabs / (i - 1)
            dataabsavg.append(dataabs)

print(dataavg)
x = range(1,h+1)
os.makedirs('avg_img')
os.makedirs('avg_txt')
path = os.getcwd()
dir_name = os.path.basename(path)
for i in range(0, len(cols)):
    out_file = open("avg_txt/" + dir_name + "_" + cols[i] + '.dat', 'w')
    y = list()
    for j in range(0, h):
        y.append(dataavg[j][i])
        out_file.write("%e\n" % (dataavg[j][i]))
    out_file.close()
    plt.figure(figsize=(7, 5))

    plt.plot(x, y, '-o')
    plt.ylabel(cols[i])
    plt.tight_layout()
    plt.savefig("avg_img/" + dir_name + "_" + cols[i] + ".png", dpi=96)
    plt.close()

linestyles = ('-o','--o','-.o',':o','-s','--s','-.s',':s','-^','--^','-.^',':^')
for avgname in list_avg:
    ll = 0
    plt.figure(figsize=(10, 5))
    ax = plt.subplot(121)
    for i in range(0, len(cols)):
        if avgname in cols[i]:
            y = list()
            for j in range(0, h):
                y.append(dataavg[j][i])
            ax.plot(x, y, linestyles[ll%12], label=cols[i])
            ll += 1
            plt.ylabel(avgname)

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
    plt.show()
    plt.savefig("avg_img/" + dir_name + "_0PLANES" + avgname + ".png", dpi=96)
    plt.close()

k=0
comb_matrix_slip = [3, 3, 12]
comb_matrix_slip_names = ['basal slip', 'prism slip', 'pyramidal slip']
comb_matrix_twin = [6, 6, 6]
comb_matrix_twin_names = ['{10.2}', '{11.1}', '{11.2}']
comb_matrix = list()
list_comb = ['_resistance_', '_shearrate_','_resolvedstress_']
add_type = ['true', 'abs']
for addtype in add_type:
    if addtype == 'true': dataavg0 = dataavg
    if addtype == 'abs': dataavg0 = dataabsavg
    for def_type in ['slip', 'twin']:
        comb_matrix = eval('comb_matrix_' + def_type)
        sys_name = eval('comb_matrix_' + def_type + '_names')
        for combname in list_comb:
            ll = 0
            k = 0
            plt.figure(figsize=(10, 5))
            ax = plt.subplot(121)
            for comb_len in comb_matrix:
                z = list()
                for j in range(1, comb_len + 1):
                    kj = k + j
                    for i in range(0, len(cols)):
                        if str(kj) + combname + def_type == cols[i]:
                            print(str(kj) + combname + def_type)
                            y = list()
                            for jj in range(0, h):
                                y.append(dataavg0[jj][i])
                            break
                    if len(z) == 0:
                        z = y
                    else:
                        z = [sum(xx) for xx in zip(z, y)]
                ax.plot(x, z, linestyles[ll % 12],
                        label=sys_name[ll])
                ll += 1
                plt.ylabel(combname + def_type + '_' + addtype)
                plt.title(def_type + ' matrix is ' + str(comb_matrix))
                k += comb_len
            ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
            plt.savefig("avg_img/" + dir_name + "_0SYSTEMS_" + addtype + combname + def_type + ".png", dpi=96)
            plt.close()

ll = 0
jjj = 0
z = list()
sumz = list()
for def_type in ['slip', 'twin']:
    k = 0
    combname = '_shearrate_'
    comb_matrix = eval('comb_matrix_' + def_type)
    for comb_len in comb_matrix:
        y = list()
        zz = list()
        for j in range(1, comb_len + 1):
            kj = k + j
            for i in range(0, len(cols)):
                if str(kj) + combname + def_type == cols[i]:
                    print(str(kj) + combname + def_type)
                    y = list()
                    for jj in range(0, h):
                        y.append(dataabsavg[jj][i])
                if len(zz) == 0:
                    zz = y
                else:
                    zz = [sum(xx) for xx in zip(zz, y)]
        z.append(zz)
        k += comb_len
plt.figure(figsize=(10, 5))
ax = plt.subplot(121)
sumz = z[0]
sys_name = comb_matrix_slip_names + comb_matrix_twin_names
for i in range(1, len(z)):
    sumz = [sum(xx) for xx in zip(sumz, z[i])]
for i in range(0, len(z)):
    for k in range(0, len(z[0])):
        z[i][k] = z[i][k] / sumz[k]
    ax.plot(x, z[i], linestyles[ll % 12], label=sys_name[ll])
    ll += 1
    plt.ylabel('Relative activity')
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
plt.savefig("avg_img/" + dir_name + "_0REL_ACTIVITY" + ".png", dpi=96)
plt.close()
