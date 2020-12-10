import sys
ratio_file = sys.argv[1]
LOH_file = sys.argv[2]

fo = open(LOH_file, 'w')
for line in open(ratio_file):
    line = line.strip()
    cols = line.split('\t')
    ratio = float(cols[5])
    if ratio < 0.1:
        fo.write(line + '\n')
    else:
        fo2.write(line + '\n')


