from matplotlib import pyplot as plt
from matplotlib import cycler
from matplotlib.ticker import MaxNLocator
import numpy as np
import csv


from constants import *


def get_mutations(li, min_, max_):
	m = []
	for x in li:
	    if min_ <= x <= max_:
	        m.append(x)
	return m
    
    
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
     
     
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
variations = []

with open('./data/gor4', newline='\n') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        while '' in row:
            row.remove('')
        data.append(np.array(row[1:4]).astype(np.float32))
data = np.array(data[:-1])

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

with open('./data/biomuta.csv', newline='\n') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader, None)  # skip the headers
    for row in reader:      
        while '' in row:
            row.remove('')
        variations.append(int(row[5]))
        
flex = np.loadtxt('./data/flex9.txt')
scores = flex.T[1]
aa_pos = flex.T[0]
high_flex_aa = []
high_flex = []
for pos, score in enumerate(scores):
    if score > FLEX_SCORE:
        high_flex_aa.append(pos)
        high_flex.append(score)
        
        
plt.hist(variations, bins=AA_NUMBER)
ax = plt.gca()
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

mutations_dynamic = []
mutations_flex = []
mutations_dynamic_flex = 0

# dynamic substructures
ax.fill_between(range(100,101), 0, 3, color='blue', alpha=.2, label="dynamic")
for var_ in var_structures:
    ax.fill_between(range(var_[0][0], var_[-1][0] + 1), 0, 3, color='blue', alpha=.2)
    mutations_dynamic += get_mutations(variations, var_[0][0], var_[-1][0])


# flexible substructures
for x in [3,4,4]: high_flex_aa.pop(x); 

for pos in high_flex_aa:
    pos = int(pos)
    if pos == int(high_flex_aa[0]):
        ax.fill_between(range(2, int(aa_pos[pos+4])), 0, 3, color='green', alpha=.2, label="high flexibility")
        mutations_flex += get_mutations(variations, 2, int(aa_pos[pos+4]))
    else:
        ax.fill_between(range(int(aa_pos[pos-4]), int(aa_pos[pos+4])), 0, 3, color='green', alpha=.2)
        mutations_flex += get_mutations(variations, int(aa_pos[pos-4]), int(aa_pos[pos+4]))
     

n = len(variations)
intersected = 0
print(intersection(mutations_dynamic, mutations_flex))
for m in intersection(mutations_dynamic, mutations_flex):
    print(variations.count(m))
    intersected += variations.count(m)
mutations_dynamic_flex = len(mutations_dynamic) + len(mutations_flex) - 2 * intersected
print('Dynamic:', str(len(mutations_dynamic)), str(len(mutations_dynamic)*100/n) + '%')
print('Flex:', str(len(mutations_flex)), str(len(mutations_flex*100)/n) + '%')
print('Total:', str(mutations_dynamic_flex), str(mutations_dynamic_flex*100/n) + '%')  

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(0.9, 0.8))
plt.xlabel("Amino acid position")
plt.ylabel("Frequency of variations")
plt.show()

