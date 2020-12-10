import sys

infile = sys.argv[1]
outfile = sys.argv[2]

fo = open(outfile, 'w')
fo.write('BLOCK' + '\n')
for line in open(infile):
    line = line.strip() 
    if line[0] == '#':
        continue
    cols = line.split('\t')
    chrom = 'chr' + cols[0]
    pos = cols[1]
    ref = cols[3]
    alt = cols[4]
    gt = cols[9]
    if gt == '0|0' or gt == '1|1':
        continue
    cols2 = gt.split('|')
    allele_1 = cols2[0]
    allele_2 = cols2[1]
    fo.write('.\t' + allele_1 + '\t' + allele_2 + '\t' + chrom + '\t' + pos + '\t' + ref + '\t' + alt + '\t' + '0/1' + '\t.\t.\t.\t.\n')
fo.write('********\n')

