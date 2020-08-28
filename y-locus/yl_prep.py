import os
from shutil import copyfile, rmtree
import numpy as np

tg_dir = "sae304three"

var_range = np.array([0, 45, 90])
sim_files = [".config", ".geom"]
for i in range(0, len(var_range)):
    work_dir = tg_dir+"_"+str(var_range[i])
    if os.path.exists(work_dir):
        rmtree(work_dir, ignore_errors=True)
    os.makedirs(work_dir)
    lst = os.listdir(tg_dir)
    for file in sim_files:
        for filename in lst:
            if filename.endswith(file):
                copyfile(tg_dir + "/" + filename, work_dir+"/" + filename)

    f1 = open(work_dir + "/locus" + "_"+str(var_range[i]) + ".load", 'w')
    if var_range[i] == 0:
        f1.write("fdot 0.05 0 0  0 * 0   0 0 *  stress  * * *   * 0 *   * * 0  time 1  incs 500 freq 5")
    elif var_range[i] == 45:
        f1.write("fdot 0.05 0 0  0 0.05 0   0 0 *  stress  * * *   * * *   * * 0  time 1  incs 500 freq 5")
    elif var_range[i] == 90:
        f1.write("fdot * 0 0  0 0.05 0   0 0 *  stress  0 * *   * * *   * * 0  time 1  incs 500 freq 5")
    else:
        raise ValueError('This angle is not yet supported.')  # TODO!

    f1.close()
