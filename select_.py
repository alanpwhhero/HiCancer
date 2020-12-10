import sys

CHROMSOME = sys.argv[1]
infile = sys.argv[2]
outfile = infile + '_' + CHROMSOME

fo = open(outfile, 'w')

for line in open(infile):
    line = line.strip()
    if line[0] == '@':
        fo.write(line + '\n')
        continue
    cols = line.split('\t')
    chrom = cols[2]
    if chrom == CHROMSOME:
        fo.write(line + '\n')


