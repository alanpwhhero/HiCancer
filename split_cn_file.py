import sys
infile = sys.argv[1]

blocks = []
for line in open(infile):
    line = line.strip()
    if line[0:5] == 'BLOCK':
        block = []
        block.append(line)
    elif line[0] == '*':
        block.append(line)
        blocks.append(block)
    else:
        block.append(line)
block.append('********')
blocks.append(block)

prefix = infile
chrom_blocks = {}
for block in blocks:
    cols = block[1].split('\t')
    chrom = cols[3]
    print(chrom)
    if chrom not in chrom_blocks:
        chrom_blocks[chrom] = []
    chrom_blocks[chrom].append(block)

for chrom in chrom_blocks:
    fo = open(prefix + '_' + chrom, 'w')
    for block in chrom_blocks[chrom]:
        for line in block:
            fo.write(line + '\n')
    fo.close() 

