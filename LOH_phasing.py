import os
import sys
CHROM = sys.argv[1]
output_dir = sys.argv[2]

LOH_list = []
nonLOH_list = []

for line in open(output_dir + '/' + CHROM+'_LOH_nonLOH_regions'):
    line = line.strip()
    cols = line.split('\t')
    start = int(cols[0])
    end = int(cols[1])
    ty = cols[2]
    if ty == 'LOH':
        LOH_list.append((start, end, ty))
    if ty == 'nonLOH':
        nonLOH_list.append((start, end, ty))
    
merged_list = LOH_list + nonLOH_list
merged_list.sort()

index = {}
num_LOH = 0
num_nonLOH = 0
for i in range(len(merged_list)):
    (start, end, ty) = merged_list[i]
    if ty == 'LOH':
        index[i] =  num_LOH
        num_LOH += 1
    else:
        index[i] =  num_nonLOH
        num_nonLOH += 1


counts = {}
for line in open(output_dir + '/' + CHROM+'_graph'):
    line = line.strip()
    cols = line.split('\t')
    nonLOHindex = int(cols[0])
    allele = int(cols[1])
    LOHindex = int(cols[2])
    value = int(cols[3])
    counts[(nonLOHindex, allele, LOHindex)] = value

phasing = {}

if merged_list[0][2] == 'LOH':
    phasing[0] = 2
else:
    phasing[(0,1)] = 1
    phasing[(0,2)] = 2


for i in range(1, len(merged_list)):
    (start, end, ty) = merged_list[i]
    (last_start, last_end, last_ty) = merged_list[i-1]
    this_index = index[i]
    last_index = index[i-1]

    if ty == 'LOH':
        if counts[(last_index, 1, this_index)] > counts[(last_index, 2, this_index)]:
            phasing[this_index] = phasing[(last_index, 1)]
        else:
            phasing[this_index] = phasing[(last_index, 2)]
    else:
        if counts[(this_index, 1, last_index)] > counts[(this_index, 2, last_index)]:
            phasing[(this_index,1)] = phasing[last_index]
            phasing[(this_index,2)] = 3 - phasing[last_index]
        else:
            phasing[(this_index,2)] = phasing[last_index]
            phasing[(this_index,1)] = 3 - phasing[last_index] 
 
fp = open(output_dir + '/' + CHROM + '_phasing', 'w')
for key in phasing:
    allele = phasing[key]
    if type(key) is not tuple:
        fp.write(str(key) + '\t' + str(allele) + '\n')
    else:
        fp.write(str(key[0]) + ' ' + str(key[1]) + '\t' + str(allele) + '\n')

