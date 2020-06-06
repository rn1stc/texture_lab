import os
from shutil import rmtree
scratch_path = '/mnt/pool/1/dimazhuk'
sh_dir = 'sh_autosolve'
if os.path.exists(sh_dir):
    rmtree(sh_dir)
    os.makedirs(sh_dir)
else:
    os.makedirs(sh_dir)

folders = sorted(next(os.walk(scratch_path))[1])
print folders
f_run = open(sh_dir + '/run_autosolve', 'w')
for folder in folders:
    mc_path = scratch_path + '/' + folder + '/material.config'
    if os.path.isfile(mc_path):
        geom = list()
        load = list()
        files_list = os.listdir(scratch_path + '/' + folder)
        for file0 in files_list:
            if file0.endswith(".geom"):
                geom.append(file0)
            if file0.endswith(".load"):
                load.append(file0)
        if len(geom) == 1 and len(load) == 1:
            f1 = open(sh_dir + '/solve_' + folder + '.sh', 'w')
            f1.write('#!/bin/bash\n#\n#PBS -l nodes=1:ppn=16,walltime=6:00:00:00\n')
            f1.write('export PETSC_DIR=' + scratch_path + '/petsc-3.6.4\nexport PETSC_ARCH=mpif90\n')
            f1.write('source ' + scratch_path + '/DAMASK/DAMASK_env.sh\nexport DAMASK_NUM_THREADS=16\n')
            f1.write('export PATH=' + scratch_path + '/petsc-3.6.4/gfortran/bin:$PATH\n')
            f1.write('export LD_LIBRARY_PATH=' + scratch_path + '/petsc-3.6.4/gfortran/lib:$LD_LIBRARY_PATH\n')
            f1.write('cd ' + scratch_path + '/%s\nrm -rf postProc\n' % folder)
            f1.write('mpirun ' + scratch_path + '/DAMASK/bin/DAMASK_spectral --geom %s' % str(geom[0]))
            f1.write(' --load %s |& tee terminal.out\n' % str(load[0]))
            f1.write('source ' + scratch_path + '/DAMASK/oldcore/bproc_twf |& tee bproc.out\n')
            f1.write('python ' + scratch_path + '/DAMASK/oldcore/dam_avg.py |& tee avg.out\n')
            f1.write('python ' + scratch_path + '/DAMASK/oldcore/spec2odf.py |& tee spec2odf.out')
            f1.close()
            f_run.write('qsub ' + os.getcwd() + '/' + sh_dir + '/solve_' + folder + '.sh\n')
        else:
            print 'Directory ' + folder + ' has ' + str(len(geom)) + ' geom files and ' + str(len(load)) + \
                  ' load files while only one set is allowed. Omitting...'
f_run.write('showq')
f_run.close()
