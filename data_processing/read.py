from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import os
import math
import re
import matplotlib.pyplot as plt
import numpy as np

path = "d:\\texture\\dat\\"

## Замена директории
#retval = os.getcwd()
#print ("Текущая директория %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Смена директории: %s" % retval)

filename = input("Введите номер файла (без расширения) \n")
file = filename + ".dat"

#checking if file
while not os.path.exists(file):
    print ("Файл не найден. Попробуйте еще раз.")
    filename = input("Введите номер файла (без расширения)\n")
    file = filename + ".dat"
else:
    print ("Файл " + file + " обнаружен.\n")


#open and read the header
f = open(file)
ii = 0
while ii < 8:
   line = f.readline()
   info = re.findall(r'\w*.\w*',line)
   info = ''.join(info)
   info = re.sub(r'^\s','',info)
   info = re.sub(r':\s*','  :   ',info)
   print(info)
   ii = ii+1

nul = f.readline()
nul = re.findall('\d+', nul)
aver_nul = 0
for i in range(len(nul)):
    zz = int(nul[i])
    aver_nul = aver_nul + zz
aver_nul = aver_nul/len(nul) #Средняя интенсивность в нуле
#print(aver_nul)

f.readline()
line = []
line_val = []
intens = []

## Считывание интенсивности (каждый угол наклона отдельной строкой)
while True:
    line=f.readline()
    if line == '\n':
        intens.append(line_val)
        line_val = []
    else:
        line_val.extend(re.findall('\d+', line))
    if not line: break

## Фон
fon = []; lnum = len(intens); lnum2 = len(intens[lnum-1])
for i in range(lnum2):
    fon.append(intens[lnum-1][i])
#print(fon)
intens.pop()
#intens.insert(0,aver_nul)
#print(intens)
f.close() #Взяли из файла все, что могли. Теперь открываем defocs

defocs_file = 'defocs.dat'
defocs = open(defocs_file)
defocs.readline()
def_th = defocs.readline()
def_th = re.findall('\d+.\d+', def_th) #Углы тета
#print(def_th)

## Забиваем коэффициенты в список
kor = []
while True:
    def_line=defocs.readline()
    kor.append(re.findall('\d+.\d+', def_line))
    if not def_line: break
#print(kor)
    
## Находим нужные коэффициенты
theta = input("Введите угол 2theta\n")
kk = 0
Bingo = 0

#Проверка на число
def isfloat(a):
    try:
        float(a)
        return True
    except (TypeError,ValueError):
        return False

while not isfloat(theta):
    theta = input("Некорректный угол! Введите угол 2theta\n")    

while (float(theta) > 193 or float(theta) < 39.6) and isfloat(theta):
  theta = input("Некорректный угол! Введите угол 2theta\n") #Почему это вообще работает?
else:
  while float(theta) >= float(def_th[kk]):
      if float(theta) == float(def_th[kk]):
          Bingo = 1
          break
      #print(def_th[kk])
      kk = kk+1
del_x = float(def_th[kk]) - float(def_th[kk-1])
koef = []    #Находим столбец коэффициентов с помощью линейной интерполяции
#print (del_x)
if not Bingo:
  for i in range(len(kor)-1):
      koefA = ((float(kor[i][kk+1]) - float(kor[i][kk]))/del_x) #(Ax + B)
      koefB = float(kor[i][kk+1]) - float(koefA)*float(def_th[kk])
      koefN = float(koefA)*float(theta)+float(koefB)
      koef.append(koefN)
      #print(koefA,koefB)
else:        #Если угол точно равен значению из файла
  for i in range(len(kor)-1):
      koef.append(kor[i][kk+1])
#print(koef)

## Непосредственно расчет
#tilt = 90  
tilt = (len(intens))*5 #угол наклона подсчитывается автоматически
#print("Угол наклона " + str(tilt) + " градусов")
s_tilt = 5 #шаг наклона
s_rot = 5  #шаг поворота
psi = [math.radians(i*5) for i in range(0,int(tilt/s_tilt+1))]
phi = [math.radians(i*5) for i in range(0,72)]

#print(fon,intens[0])
fintens = [] #Вычесть фон, умножить на поправку
aver_nul = (float(aver_nul) - float(fon[0]))*koef[0]
#kkk = 0
for i in range(len(intens)):
    for j in range(len(intens[i])):
        fintens.append((float(intens[i][j])-float(fon[i+1])) * float(koef[i+1]))
        #print(intens[i][j],fon[i+1],koef[i+1],fintens[kkk])
        #kkk = kkk + 1
#fintens.insert(0,aver_nul)
#print(fintens)

## подсчитать площадь

def cosin(angl,spsi,sphi): #подсчет косинусов
    if math.degrees(angl) < 90: #для углов меньше 90
        answer = sphi*(math.cos(angl - 0.5*math.radians(spsi)) - math.cos(angl + 0.5*math.radians(spsi)))
        return answer
    elif math.degrees(angl) >= 90: #Если угол равны 90
        answer = sphi*math.cos(angl - 0.5*math.radians(spsi))
        return answer

omega = [] #Список для площади каждой точки
omega00 = []
for i in range(1,len(psi)):
       for j in range(len(phi)):
          omega.append(cosin(psi[i],s_tilt,s_rot))
for i in range(len(phi)):
    omega00.append(360*s_rot*(1 - math.cos(0.5*math.radians(s_tilt))))
#print(omega00)

aver_nul00 = []
for i in range(len(phi)):
    aver_nul00.append(360*aver_nul*s_rot*(1 - math.cos(0.5*math.radians(s_tilt))))
#print(aver_nul00)
#print(len(fintens),len(omega))

norm = [] #Нормировочный коэффициент (сумма)
ko = 0
for i in range(1,len(psi)):
    for j in range(len(phi)):        
        norm.append(fintens[ko] * cosin(psi[i],s_rot,s_tilt))
        #print(fintens[ko],math.degrees(psi[i]),norm[ko])
        ko = ko + 1
omega0s = sum(omega00)
norm0s = sum(aver_nul00)
omega.insert(0,omega0s)
norm.insert(0,norm0s)

norm_koef = sum(norm)/sum(omega)
print(len(norm),len(omega),norm_koef)

## Полюсная плотность
Pdens = []
kok = 0
for i in range(1,len(psi)):
    for j in range(len(phi)):
        Pdens.append(fintens[kok]/norm_koef)
        kok = kok + 1
P0 = aver_nul / norm_koef
Pdens.insert(0,P0)
print(norm0s,aver_nul,P0)

x = []
y = []

## координаты
for N in range(1,len(psi)):
    for M in range(len(phi)):
        x.append(math.tan(psi[N]/2)*math.sin(phi[M]))
        y.append(math.tan(psi[N]/2)*math.cos(phi[M]))
x.insert(0,0); y.insert(0,0)
#print(x,y)

#for i in range(len(x)):
#    print(str('%4f' % x[i]) + "   " + str('%4f' % y[i]) + "   " + str('%4f' % Pdens[i]))
#print(len(Pdens),len(x),len(y))

#writing down to the file in new directory
path2 = "d:\\texture\\pyth\\"
os.chdir( path2 )
newfile = filename + "s" + ".dat"
f = open(newfile, 'w')
k = 0
for i in range(len(x)):
    f.write(str('%3f' % x[i]) + "    " + str('%3f' % y[i]) + "    " + str('%3f' % Pdens[i]) + "\n")
f.close()
if os.path.exists(newfile):
    print('Файл с результатом обработки записан:\n' + path2 + newfile)
    wannadraw = input("Желаете посмотреть результат? (y/n) \n")
    if wannadraw == "y":
        #f = open(newfile)
        #ar = np.fromfile(f, dtype=float, count=-1, sep=' ') #build an array from file
        #count = len(ar)/4
        #ar.shape = (int(count),4)
        #print(ar.shape) #just to be shure, shape of an array should be (1079,4): (x,y,z,tilt_angle)
        npts = 200
        Numofcont = input("Введите число контуров \n")
        #define data
        #x = ar[:,0]
        #y = ar[:,1]
        z = Pdens
        # define grid.
        xi = np.linspace(-0.81, 0.81, 100)
        yi = np.linspace(-0.81, 0.81, 200)
        # grid the data.
        zi = griddata(x, y, z, xi, yi, interp='linear')
        # contour the gridded data, plotting dots at the nonuniform data points.
        CS = plt.contour(xi, yi, zi, int(Numofcont), linewidths=0.5, colors='k')
        CS = plt.contourf(xi, yi, zi, int(Numofcont),
                          vmax=abs(zi).max(), vmin=0,cmap='inferno')
        plt.colorbar()  # draw colorbar
        # plot data points.
        #plt.scatter(x, y, marker=',', s=1, zorder=10)
        Max_x = np.amax(x) - 0.005
        Max_xx = Max_x + 0.15
        Max_xxx = Max_xx + 0.05
        plt.xlim(-float(Max_xxx), float(Max_xxx))
        plt.ylim(-float(Max_xxx), float(Max_xxx))
        circle1 = plt.Circle((0, 0), float(Max_x), color='k', fill=False, linewidth=2)
        circle2 = plt.Circle((0, 0), float(Max_xx), color='k', fill=False, linewidth=1.5)
        plt.gcf().gca().add_artist(circle1)
        plt.gcf().gca().add_artist(circle2)
        plt.title('Pole figure for file ' + filename)
        plt.show()   
else:
    print('Файл не создан. Перезапустите программу и попробуйте снова')

dontgo = input("Нажмите Enter, чтобы закрыть программу")
