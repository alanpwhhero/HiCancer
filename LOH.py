import sys
snp_file = sys.argv[1]
ratio_file = sys.argv[2]

chrom_lines = {}
for line in open(snp_file):
    line = line.strip()
    if line[0] == '#':
        continue
    cols = line.split('\t')
    chrom = cols[0]
    pos = int(cols[1])
    block_i = int(pos / 1000000)
    if chrom not in chrom_lines:
        chrom_lines[chrom] = []
    if block_i > len(chrom_lines[chrom]) - 1:
        len_chrom_lines = len(chrom_lines[chrom])
        for k in range(block_i - len_chrom_lines + 1):
            chrom_lines[chrom].append([]) 
    chrom_lines[chrom][block_i].append(line)

fo = open(ratio_file, 'w')
for chrom in chrom_lines:
    for block_i in range(len(chrom_lines[chrom])):
        block = chrom_lines[chrom][block_i]
        num_homo = 0
        num_hetero = 0

        for line in block:
            cols = line.split('\t')
            vtype = cols[10]
            if vtype == 'homo':
                num_homo += 1
            else:
                num_hetero += 1
        start = block_i * 1000000
        end = (block_i + 1) * 1000000
        
        total = num_homo + num_hetero
        if total > 0:
            ratio = num_hetero / total
        else:
            ratio = -1
        fo.write(chrom + '\t' + str(start) + '\t' + str(end) + '\t' + str(num_homo) + '\t' + str(num_hetero) + '\t' + str(ratio) + '\n')


