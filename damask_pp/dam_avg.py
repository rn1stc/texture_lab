#!/usr/bin/env python3
#############################################################
# version = 2020-03-11   (YYYY-MM-DD)
#
#
#############################################################

import csv, os, glob, shutil, math
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


for directory in ['avg_img', 'avg_txt']:
    if os.path.isdir(directory):
        shutil.rmtree(directory, ignore_errors=True)   # clear previous output
    os.makedirs(directory)

list_avg = ['_eulerangles', '_f', '_p', '_resistance_slip', '_shearrate_slip','_resolvedstress_slip',
            '_resistance_twin', '_shearrate_twin', '_resolvedstress_twin', '_resistance', '_shearrate',
            '_resolvedstress', 'accumulatedshear_twin']
dataavg = list()
dataabsavg = list()
lst = os.listdir('.')
lst.sort()
h = len(glob.glob1('.',"*.txt")) - len(glob.glob1('.',"*nodal.txt"))
for filename in lst:
    if filename.endswith('.txt') and not filename.endswith('nodal.txt'):
        with open(filename, 'rt') as f:
            headersize = int(f.readline()[0])
            for i in range(1, headersize):
                next(f)
            reader = csv.reader(f, delimiter='	', skipinitialspace=True)

            cols = next(reader)
            w = len(cols)
            #print(cols)
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

#print(dataavg)
x_axis_var = '9_f'
var_ind = cols.index(x_axis_var)
end_x_var = abs((dataavg[h-1][cols.index(x_axis_var)] * 100 - 100))
print("end_x_var ", end_x_var)
# x = range(1,h+1)
x = np.linspace(0, end_x_var, num = h)
# x = x.tolist()

dir_name = os.path.basename(os.path.abspath(os.path.join(__file__ ,"../..")))
for i in range(0, len(cols)):
    out_file = open("avg_txt/"  + cols[i] + '.dat', 'w')
    y = list()
    for j in range(0, h):
        y.append(dataavg[j][i])
        out_file.write("%e\n" % (dataavg[j][i]))
    out_file.close()
    plt.figure(figsize=(5, 3))

    plt.plot(x, y, '-o')
    plt.ylabel(cols[i])
    plt.xlabel(u"Деформация, %")
    plt.tight_layout()
    plt.savefig("avg_img/" + cols[i] + ".png", dpi=96)
    plt.close()

linestyles = ("-","--","-.",":","x","+",".","d","^","p","_","h")
for avgname in list_avg:
    ll = 0
    plt.figure(figsize=(5, 3))
    ax = plt.subplot(121)
    for i in range(0, len(cols)):
        if avgname in cols[i]:
            y = list()
            for j in range(0, h):
                y.append(dataavg[j][i])
            ax.plot(x, y, linestyles[ll%12], label=cols[i])
            ll += 1
            plt.ylabel(avgname)
            plt.xlabel(u"Деформация, %")
            plt.tight_layout()

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
    plt.show()
    plt.savefig("avg_img/" + "0PLANES" + avgname + ".png", dpi=96)
    plt.close()

k=0
comb_matrix_slip = [12] #[3, 3, 12]
comb_matrix_slip_names = [u'базисное', u'призматическое', u'пирамидальное']
comb_matrix_twin = [12] #[6, 6, 6]
comb_matrix_twin_names = [r'{10$\bar 1$2}', r'{11$\bar 2$1}', r'{11$\bar 2$2}']
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
            plt.figure(figsize=(5, 3))
            ax = plt.subplot(121)
            for comb_len in comb_matrix:
                z = list()
                for j in range(1, comb_len + 1):
                    kj = k + j
                    for i in range(0, len(cols)):
                        if str(kj) + combname + def_type == cols[i]:
                            #print(str(kj) + combname + def_type)
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
                plt.xlabel(u"Деформация, %")
                plt.title(def_type + ' matrix is ' + str(comb_matrix))
                plt.tight_layout()
                k += comb_len
            ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
            plt.savefig("avg_img/" + "0SYSTEMS_" + addtype + combname + def_type + ".png", dpi=96)
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
                    #print(str(kj) + combname + def_type)
                    y = list()
                    for jj in range(0, h):
                        y.append(dataabsavg[jj][i])
                if len(zz) == 0:
                    zz = y
                else:
                    zz = [sum(xx) for xx in zip(zz, y)]
        z.append(zz)
        k += comb_len
plt.figure(figsize=(5, 3))
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
    plt.ylabel(u"Отн. акт систем")
    plt.xlabel(u"Деформация, %")
    plt.tight_layout()
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
plt.savefig("avg_img/" + "0REL_SHEAR_ACTIVITY" + ".png", dpi=96)
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
                    #print(str(kj) + combname + def_type)
                    y = list()
                    for jj in range(0, h):
                        if def_type == "slip":
                            y.append(dataabsavg[jj][i])
                        elif def_type == "twin":
                            if kj < 7:
                                y.append(dataabsavg[jj][i] * 19)
                            elif kj < 13:
                                y.append(dataabsavg[jj][i] * 9)
                            else:
                                y.append(dataabsavg[jj][i] * 2)
                if len(zz) == 0:
                    zz = y
                else:
                    zz = [sum(xx) for xx in zip(zz, y)]
        z.append(zz)
        k += comb_len
plt.figure(figsize=(5, 3))
ax = plt.subplot(121)
total_by_sys = list()
for i in range(0, len(z)):
    total_by_sys.append(sum(z[i]))
total_by_sys = total_by_sys / sum(total_by_sys)
sumz = z[0]
sys_name = comb_matrix_slip_names + comb_matrix_twin_names
for i in range(1, len(z)):
    sumz = [sum(xx) for xx in zip(sumz, z[i])]
out_file_rel = open('avg_txt/rel_sys_act.dat', 'w')
for i in range(0, len(z)):
    for k in range(0, len(z[0])):
        z[i][k] = z[i][k] / sumz[k]
    ax.plot(x, z[i], linestyles[ll % 12], label=(sys_name[ll] )) #+ " %2d%%" % (total_by_sys[ll]*100)))
    for item in z[i]:
        out_file_rel.write("{:.4f}  ".format( item ))
    out_file_rel.write("\n")
    ll += 1
    plt.ylabel(u"Отн. акт. систем")
    plt.xlabel(u"Деформация, %")
    plt.tight_layout()
out_file_rel.write("Strain:\n")
for item in x:
    out_file_rel.write("{:.4f}  ".format(item))
out_file_rel.close()
out_file_rel = open('avg_txt/rel_sys_act.dat', 'r')
print(out_file_rel.read())
out_file_rel.close()
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
plt.savefig("avg_img/" + "0REL_TEX_ACTIVITY" + ".png", dpi=96)
plt.close()
