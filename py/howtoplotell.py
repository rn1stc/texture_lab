import numpy as np
from matplotlib import patches
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

#plotting
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
for direction in ["left","bottom"]:
    ax.spines[direction].set_position('zero')
    ax.spines[direction].set_smart_bounds(True)
for direction in ["right","top"]:
    ax.spines[direction].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True)
for p in [
    patches.Ellipse(
        (0, 0), 2, 1, angle=-45, fill=False,
        edgecolor=None      
    ),
    #patches.Ellipse(
    #    (0, 0), 3, 6, angle=0, fill=False,
    #    edgecolor="red"     
    #),
]:
    ax.add_patch(p)
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.show()
