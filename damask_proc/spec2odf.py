import csv
import os

lst = os.listdir('.')
lst.sort()
print(lst)
os.makedirs('odf')
for filename in lst:
    if filename.endswith('.txt'):
        with open(filename, 'rt') as f:
            next(f)
            next(f)
            next(f)
            next(f)
            reader = csv.reader(f, delimiter='	', skipinitialspace=True)
            lineData = list()

            cols = next(reader)
            print(cols)

            for col in cols:
                # Create a list in lineData for each column of data.
                lineData.append(list())

            e1 = cols.index('1_eulerangles')
            e2 = cols.index('2_eulerangles')
            e3 = cols.index('3_eulerangles')
            vol = cols.index('volume')
            volavg = list()
            volumes = list()
            euler1 = list()
            euler2 = list()
            euler3 = list()
            for line in reader:
                volumes.append(float(line[vol]))
                euler1.append(float(line[e1]))
                euler2.append(float(line[e2]))
                euler3.append(float(line[e3]))
            filename2 = 'odf/' + filename[:-4] + '.linodf'
            f2 = open(filename2, 'w')
            f2.write("phi1   PHI   phi2   intencity\n")
            for i in range(0,len(volumes)):
                f2.write("%6.2f   %6.2f   %6.2f   %6.2f\n" % (euler1[i], euler2[i], euler3[i], 1.0))
            f2.close()
