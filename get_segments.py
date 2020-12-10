import sys
CHROM = sys.argv[1]
N = int(sys.argv[2])
phased_file = sys.argv[3]
output_dir = sys.argv[4]

threshold = 1000000
blocks = []
for line in open(phased_file):
    line = line.strip()
    if line[0:5] == 'BLOCK':
        block = []
    elif line[0] == '*':
        blocks.append(block)
    else:
        block.append(line)

LOH_itvls_pre = []
LOH_itvls = []
nonLOH_itvls = []
last_end = 0
for i in range(len(blocks)):
    block = blocks[i]
    start_line = block[0]
    start_cols = start_line.split('\t')
    start = int(start_cols[4])    
    end_line = block[len(block)-1]
    end_cols = end_line.split('\t')
    end = int(end_cols[4])
    nonLOH_itvls.append((start, end))
    if i == 0:
        LOH_itvls_pre.append((0, start-1))
    else:
        LOH_itvls_pre.append((last_end + 1, start-1))

    last_end = end

LOH_itvls_pre.append((last_end, N))

for i in range(len(LOH_itvls_pre)):
    (start, end) = LOH_itvls_pre[i]
    if i == 0 or i == len(LOH_itvls_pre) - 1:
        if end - start > threshold:
            LOH_itvls.append((start, end))
    else:
        LOH_itvls.append((start, end))


fo = open(output_dir + '/' + CHROM+'_LOH_nonLOH_regions', 'w')
for (start, end) in LOH_itvls:
    fo.write(str(start) + '\t' + str(end) + '\tLOH\n')

for (start, end) in nonLOH_itvls:
    fo.write(str(start) + '\t' + str(end) + '\tnonLOH\n')




