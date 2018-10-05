import os
directory = os.fsencode('.')
print(directory)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith("material.config"):
        # print(os.path.join(directory, filename))
        f1 = open(filename, "r")
        f2 = open(filename + '.ebsd', 'w')
        f2.write('x   y   z   phi1   PHI   phi2\n')
        for line in f1:
            if "(gauss)" in line:
                f2.write('1  1  1  ')
                tmp = line
                tmp = tmp.replace('(gauss)   phi1 ', '')
                tmp = tmp.replace("Phi", "")
                tmp = tmp.replace("phi2", "")
                tmp = tmp.replace("   scatter 0.0   fraction 1.0", "")
                f2.write(tmp)
        f1.close()
        f2.close()

        continue