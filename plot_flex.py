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

data = np.loadtxt('./data/flex9.txt')
scores = data.T[1]
aa_pos = data.T[0]
high_flex_aa = []
high_flex = []
for pos, score in enumerate(scores):
    if score > FLEX_SCORE:
        high_flex_aa.append(pos)
        high_flex.append(score)
plt.plot(data.T[0], data.T[1], label='Average flexibility, window=9')
for pos in high_flex_aa:
    pos = int(pos)
    if pos == int(high_flex_aa[0]):
        plt.plot(aa_pos[pos-1:pos+3], scores[pos-1:pos+3], 'g', label='High flexibility')
        print(PRIMARY[2:int(aa_pos[pos+4])])
        print(SECONDARY[2:int(aa_pos[pos+4])])
        print(str(int(aa_pos[pos-1])+1), '-', str(int(aa_pos[pos+3])+1))
        
    else:
        plt.plot(aa_pos[pos-4:pos+4], scores[pos-4:pos+4], 'g')
        print(PRIMARY[int(aa_pos[pos-4]):int(aa_pos[pos+4])])
        print(SECONDARY[int(aa_pos[pos-4]):int(aa_pos[pos+4])])
        print(str(int(aa_pos[pos-4])+1), '-', str(int(aa_pos[pos+4])+1))
plt.xlabel('Position')
plt.ylabel('Flexibility Score')
plt.title('ProtScale output for CDCA5_HUMAN')
plt.legend()
plt.show()

