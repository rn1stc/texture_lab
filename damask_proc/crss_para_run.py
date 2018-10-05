import os
from shutil import copyfile
from shutil import rmtree
import numpy as np

tg_dir = "zr_t2"
tg_type = "twin"
sat_also = "yes"
geom_name = "fourh.geom"
load_name = "rolling3x.load"
starter_name = "solve_zrext_2"

var_range = np.array([0.8, 1.2])
if tg_type == "slip":
    var_pat = [1, 2, 5]
if tg_type == "twin":
    var_pat = [1, 2, 4]
for i in range(0, len(var_range)):
    for var_num in var_pat:
        folder_name = tg_dir + "_" + tg_type + "_pat" + str(var_num) + "_" + np.array2string(var_range[i], precision=2, separator=',',)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        else:
            rmtree(folder_name)
            os.makedirs(folder_name)
        copyfile(tg_dir + "/material.config", folder_name + "/material.config.tmp")
        copyfile(tg_dir + "/" + geom_name, folder_name + "/" + geom_name)
        copyfile(tg_dir + "/" + load_name, folder_name + "/" + load_name)
        f1 = open(folder_name + "/material.config.tmp", 'r')
        f2 = open(folder_name + "/material.config", 'w')
        for line in f1:
            if line.startswith("tau0_" + tg_type):
                line_elems = np.fromstring(line[12:len(line)], dtype=float, sep='    ')
                f2.write("tau0_" + tg_type)
                for j in range(0, len(line_elems)):
                    if j == (var_num-1):
                        f2.write("    %3de6" % (line_elems[j] * var_range[i] / 1000000.0))
                    else:
                        f2.write("    %3de6" % (line_elems[j] / 1000000.0))
                f2.write("\n")
            elif line.startswith("tausat_" + tg_type) and sat_also == "yes":
                line_elems = np.fromstring(line[14:len(line)], dtype=float, sep='    ')
                f2.write("tausat_" + tg_type)
                for j in range(0, len(line_elems)):
                    if j == (var_num-1):
                        f2.write("    %3de6" % (line_elems[j] * var_range[i] / 1000000.0))
                    else:
                        f2.write("    %3de6" % (line_elems[j] / 1000000.0))
                f2.write("\n")
            else:
                f2.write(line)
        f1.close()
        f2.close()
        os.remove(folder_name + "/material.config.tmp")