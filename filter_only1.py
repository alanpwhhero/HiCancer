import sys
input_file = sys.argv[1]
output_file = sys.argv[2]


fo = open(output_file, 'w')
for line in open(input_file):
    line = line.strip()
    if line[0] == '#':
        fo.write(line + '\n')
        continue
    cols = line.split('\t')
    (chrom, pos, ID, ref, alt, qual, flt, info, fmt, k562pe) = cols
    cols2 = k562pe.split(':')
    gt = cols2[0]
    cols3 = gt.split('/')
    if cols3[len(cols3) - 1] != '1':
        continue
    if cols3[0] != '0':
        vtype = 'homo'
    else:
        vtype = 'hetero'
    fo.write(chrom + '\t' + pos + '\t' + ID + '\t' + ref + '\t' + alt + '\t' + qual + '\t' + flt + '\t' + info + '\t' + fmt + '\t' + gt + '\t' + vtype + '\n')
fo.close()


