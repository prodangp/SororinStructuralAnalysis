from matplotlib import pyplot as plt
from matplotlib import cycler
import numpy as np

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

data = np.loadtxt('./data/hidr9.txt')
plt.plot(data.T[0], data.T[1], label='Hphob./Kyte & Doolittle, window=9')
plt.xlabel('Position')
plt.ylabel('Hydropathy Score')
plt.title('ProtScale output for CDCA5_HUMAN')
plt.legend()
plt.show()

