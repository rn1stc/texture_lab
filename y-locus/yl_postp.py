import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize
from math import sin, cos
import os, csv


def ellipse_polar(theta, b, e, alp):
    return b * (1 - (e * np.cos(theta - alp)) ** 2) ** -.5


def pol2car(r, theta):
    return np.array([r * np.cos(theta), r * np.sin(theta)])


def car2pol(x, y):
    return np.array([(x ** 2 + y ** 2) ** .5, np.arctan2(y, x)])


matplotlib.use('Agg')
fig = plt.figure()
ax = fig.add_subplot(111)
scale = 0
tg_dirs = ["mono_loc_one", "mono_loc_two", "mono_loc_three"]

for tg_dir in tg_dirs:
    dirs = os.listdir('.')
    dirs.sort()
    angles = list()
    for dir0 in dirs:
        if dir0.startswith(tg_dir) and dir0 != tg_dir:
            try:
                angle = int(dir0[len(tg_dir) + 1:])
                angles.append(angle)
            except ValueError:
                print('Could not recognize angle in directory' + dir0 + '. Omitting...')
            for result in ["1_p", "2_p", "5_p"]:
                with open(dir0 + "/postProc/avg_txt/postProc_" + result + ".dat", 'rt') as f:

                    reader = csv.reader(f, delimiter='	', skipinitialspace=True)
                    exec("res_" + result + "_" + str(angle) + "=np.array([])")
                    for line in reader:
                        exec("res_" + result + "_" + str(angle) + "= np.append(res_" + result + "_" + str(angle) + ", float(line[0]))")
    x = np.linspace(0, 0.1, len(res_1_p_0), endpoint=True)
    res_at45 = (res_1_p_45 + res_5_p_45) / 1.4 + abs(res_2_p_45)
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot(x, res_1_p_0)
    ax2.plot(x, res_at45, '--')
    ax3.plot(x, res_5_p_90)

    dx = x[1]-x[0]

    x_data = np.array([0, 0, 0])
    y_data = np.array([0, 0, 0])
    res_lst = ["res_1_p_0", "res_at45", "res_5_p_90"]
    for res in res_lst:
        exec("y = " + res)
        y_prime = np.gradient(y)
        young = np.average(y_prime[:25]) / dx
        sec_02 = young * x - 0.002 * young
        idx = np.argwhere(np.diff(np.sign(y - sec_02))).flatten()
        exec("sy = " + res + "[" + str(idx) + "]")
        exec("x_sy = x[" + str(idx) + "]")
        j = res_lst.index(res)
        exec("ax" + str(j + 1) + ".plot(x_sy, sy, '*')")
        x_data[j] = sy * cos(angles[j] / 57.3)
        y_data[j] = sy * sin(angles[j] / 57.3)
    plt.savefig("yield_stresses_" + tg_dir + ".png", dpi=96)
    plt.close()
    if scale == 0:
        scale = y_data[2]
        x_data = x_data / y_data[2]
        y_data = y_data / y_data[2]
    else:
        x_data = x_data / scale
        y_data = y_data / scale
    # x_data = np.array([-1, 0, 1.3])
    # y_data = np.array([0, 0.99, 0.8])
    r_data = np.zeros(len(x_data))
    th_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        [r0, th0] = car2pol(x_data[i], y_data[i])
        r_data[i] = r0
        th_data[i] = th0

    params, params_covariance = optimize.curve_fit(ellipse_polar, th_data, r_data, p0=[0.5, 0.5, 0.78],
                                                   bounds=(0, [2, 0.95, np.pi / 2]))
    print(params)

    theta_ls = np.linspace(0, 2 * np.pi, 500)
    r_ls = ellipse_polar(theta_ls, params[0], params[1], params[2])
    #r_ls = ellipse_polar(theta_ls, 2, .5, .3)
    [x_ls, y_ls] = pol2car(r_ls, theta_ls)
    ax.plot(x_ls, y_ls)
    ax.scatter(x_data, y_data)
ax.set_aspect(aspect=1)
ax.grid(True, which='both')

# set the x-spine (see below for more info on `set_position`)
ax.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax.spines['right'].set_color('none')
ax.yaxis.tick_left()

# set the y-spine
ax.spines['bottom'].set_position('zero')

# turn off the top spine/ticks
ax.spines['top'].set_color('none')
ax.xaxis.tick_bottom()
plt.setp(ax.xaxis.get_majorticklabels(), ha="left")
plt.setp(ax.yaxis.get_majorticklabels(), va="bottom")

# plot sigy/sig0

t1 = ax.text(0.35, 0.9,  r'$\frac{\sigma^{RD}}{\sigma_{y}^{RD}}$',
             verticalalignment='bottom', horizontalalignment='right',
             transform=ax.transAxes, fontsize=20)

t1.set_bbox(dict(facecolor='white', alpha=1, edgecolor='white'))

t2 = ax.text(1, 0.25,  r'$\frac{\sigma^{TD}}{\sigma_{y}^{RD}}$',
             verticalalignment='bottom', horizontalalignment='right',
             transform=ax.transAxes, fontsize=20)

t2.set_bbox(dict(facecolor='white', alpha=1, edgecolor='white'))

plt.savefig("yield_locus.png", dpi=300)
plt.show()
#plt.close()