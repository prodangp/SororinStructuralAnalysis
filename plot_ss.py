from matplotlib import pyplot as plt
from matplotlib import cycler
import numpy as np
import csv

from constants import *


# settings for the fancy plots
plt.rcParams["font.size"] = 20
colors = cycler('color',
                ['#EE6666', '#3388BB', '#9988DD',
                 '#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('axes', facecolor='#E6E6E6', edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='black', labelsize=20)
plt.rc('ytick', direction='out', color='black', labelsize=20)
font = {
        'size'   : 20}
plt.rc('font', **font)
plt.rc('patch', edgecolor='#E6E6E6')
plt.rc('lines', linewidth=2)
plt.rcParams["figure.figsize"] = (12,8)

data = []


with open('./data/gor4', newline='\n') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        while '' in row:
            row.remove('')
        data.append(np.array(row[1:4]).astype(np.float32))
        
data = np.array(data[:-1])
ax = plt.gca()
plt.plot(data[:,0], label='H')
plt.plot(data[:,1], label='E')
plt.plot(data[:,2], label='C')
var_structures = []
var_structure = False
for idx, aa in enumerate(data):
    if max(aa) < PROBABILITY_TH:
        if not var_structure:
            var_ = []
            var_structure = True
        var_.append([idx, *aa])
    elif var_structure:
        if len(var_) >= DYNAMICAL_SUBSEQ_MIN_SIZE:
            var_structures.append(var_)
        var_structure = False

for var_ in var_structures:
    ax.fill_between(range(var_[0][0], var_[-1][0] + 1), 0, 1000, color='blue', alpha=.2)
    print(str(var_[0][0] + 1), '-', str(var_[-1][0] + 1))
    print(str(PRIMARY[var_[0][0]:(var_[-1][0]+1)])) 

ax.fill_between(range(100,101), 0, 1000, color='blue', alpha=.2, label='variable')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel('Amino acid position')
plt.ylabel('Secondary structure probability')
plt.tick_params(left = False)
ax.axes.yaxis.set_ticklabels([])
plt.show()

