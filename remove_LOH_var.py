import sys
LOH_region_file=sys.argv[1]
hapcut_file = sys.argv[2]
hapcut_file_new=sys.argv[3]

LOH = set([])
for line in open(LOH_region_file):
    line = line.strip()
    cols = line.split('\t')
    chrom = cols[0]
    start = int(cols[1])
    LOH.add((chrom, start))
blocks = []
for line in open(hapcut_file):
    line = line.strip()
    if line[0:5] == 'BLOCK':
        block = []
        block.append(line)
    elif line[0] == '*':
        block.append(line)
        blocks.append(block)
    else:
        block.append(line)
blocks.append(block)

fo = open(hapcut_file_new,'w')
new_blocks = []
for block in  blocks:
    new_block =  []
    for line in block:
        if line[0:5] == 'BLOCK' or line[0] == '*':
            new_block.append(line)
            continue
        cols = line.split('\t')
        chrom = cols[3]
        pos = int(cols[4])
        start  = int(pos/1000000) * 1000000
        if (chrom, start) not in LOH:
            new_block.append(line)
    if len(new_block) > 2:
        for line in new_block:
            fo.write(line + '\n')
        

