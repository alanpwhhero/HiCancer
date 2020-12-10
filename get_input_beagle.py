
import sys
infile = sys.argv[1]
vcf_file = sys.argv[2]
header_file = sys.argv[3]
out_file = sys.argv[4]


blocks = []
for line in open(infile):
    line = line.strip()
    if line[0:5] == 'BLOCK':
        block = []
        
    elif line[0] == '*':
        blocks.append(block)
    else:
        cols = line.split('\t')
        cols[4] = int(cols[4])
        block.append(cols)


label = {}


min_pos = 100000000000
max_pos = -1
for i in range(len(blocks)):
    block = blocks[i]
    first_pos = block[0][4]
    for cols in block:
        chrom = cols[3]
        chrom = chrom[3:]
        pos = int(cols[4])
        if pos < min_pos:
            min_pos = pos
        if pos > max_pos:
            max_pos = pos
        label[(chrom, pos)] = str(first_pos)

header = []
for line in open(header_file):
    line = line.strip()
    if line[0] == '#':
        header.append(line)
        continue
    break 

data = []
for line in open(vcf_file):
    line = line.strip()
    if line[0] == '#':
        continue
    cols = line.split('\t')
    chrom = cols[0]
    chrom = chrom[3:]
    pos = int(cols[1])
    cols[0] = chrom
    cols[1] = pos
    if (chrom, pos) not in label:
        continue
    fmt = 'GT'
    info = '0/1'
    new_cols = cols[0:8]
    new_cols.append(fmt)
    new_cols.append(info)
    data.append(new_cols)


data.sort(key = lambda x: x[1])

fo = open(out_file, 'w')

for line in header:
    fo.write(line + '\n')
for cols in data:
    for i in range(len(cols)-1):
        fo.write(str(cols[i]) + '\t')
    fo.write(str(cols[len(cols)-1]) + '\n')

