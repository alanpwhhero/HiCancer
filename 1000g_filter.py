import sys
1000g_file = sys.argv[1]
snp_file = sys.argv[2]
filtered_snp_file = sys.argv[3]

snp_set = {}
for line in open(1000g_file):
    line = line.strip()
    if line[0] == '#':
        continue
    cols = line.split('\t')
    chrom = 'chr'+cols[0]
    pos = int(cols[1])
    ref = cols[3]
    alt = cols[4]
    snp_set[(chrom, pos)] = (ref, alt)

fo = open(filtered_snp_file, 'w')
for line in open(snp_file):
    line = line.strip()
    if line[0] == '#':
        fo.write(line + '\n')
        continue
    cols = line.split('\t')
    (chrom, pos, ID, ref, alt, qual, flt, info, fmt, k562pe) = cols
    pos = int(pos)
    if (chrom, pos) not in snp_set:
        continue
    if ref != snp_set[(chrom, pos)][0] or alt != snp_set[(chrom, pos)][1]:
        continue
    fo.write(line + '\n') 


