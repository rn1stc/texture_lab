#!/usr/bin/env python3
#############################################################
# version = 2019-10-17   (YYYY-MM-DD)
#
#
#############################################################

import csv, os

cr = list()
co = list()
crn = list()
con = list()
i = 0
with open('sp_info', 'rt') as f:
    reader = csv.reader(f, delimiter='	', skipinitialspace=True)
    for line in reader:
        text_line = ''.join(filter(lambda x: (x.isalpha() or x == '_'), str(line)))
        print(text_line)
        if text_line == 'Crystallite':
            i = 1
            continue
        if text_line == 'Constitutive':
            i = 2
            continue
        if text_line == '':
            i = 0
            continue
        if i == 1:
            cr.append(text_line)
            crn.append(''.join(filter(str.isdigit, str(line))))
        if i == 2:
            co.append(text_line)
            con.append(''.join(filter(str.isdigit, str(line))))
f.close()
try:
    os.remove('sp_runpp.sh')
except OSError:
    pass
with open('sp_runpp.sh', 'w') as f_run:
    f_run.write("spfile=`find . -name '*.spectralOut'`\n")
    f_run.write("postResults --cr ")
    for item in cr[:-1]:
        f_run.write("%s," % (item))
    f_run.write("%s " % cr[-1])

    if len(co) > 0:
        f_run.write("--co ")
        for item in co[:-1]:
            f_run.write("%s," % (item))
        f_run.write("%s " % (co[-1]))
    f_run.write("--split --separation x,y,z $spfile\ncd postProc\n")
    # f_run.write("python2 $DIR\"/3Dvisualize.py\" -s ")   # uncomment to use 3Dvisualize.py functions
    # res_vars = cr + co[:-1]
    # for var in res_vars[:-1]:
    #     f_run.write("\"%s\"," % (var))
    # f_run.write("\"%s\" ./\"$f\" " % (res_vars[-1]))


    f_run.write("for f in *.txt; do\n  vtk_rectilinearGrid ./\"$f\"\ndone\n")
    f_run.write("for v in *.vtr; do\n  v2=\"${v:0:-14}.vtr\"\n  mv $v $v2\ndone\n")
    f_run.write("for v in *.vtr; do\n  vtk_addRectilinearGridData --vtk $v --data ")
    res_vars = cr + co[:-1]
    for var in res_vars[:-1]:
        f_run.write("%s," % (var))
    f_run.write("%s \"${v:0:-4}.txt\"\ndone\n" % (res_vars[-1]))
    f_run.write("for f in *.txt; do\n  addDisplacement --nodal ./\"$f\"\ndone\n")
    f_run.write("for f in *nodal.txt; do\n  vtk_addRectilinearGridData --data 'fluct(f).pos','avg(f).pos'"
                " --vtk \"${f:0:-10}.vtr\" $f \ndone\n")
f_run.close()

print(crn)
