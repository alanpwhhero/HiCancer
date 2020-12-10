import sys
CHROM = sys.argv[1]
output_dir = sys.argv[2]

LOH_list = []
nonLOH_list = []

for line in open(output_dir + '/' + CHROM+'_LOH_nonLOH_regions'):
    line = line.strip()
    cols = line.split('\t')
    start = int(cols[0])
    end = int(cols[1])
    ty = cols[2]
    if ty == 'LOH':
        LOH_list.append((start, end))
    if ty == 'nonLOH':
        nonLOH_list.append((start, end))
    
counts = {}
for i in range(len(nonLOH_list)):
    for j in [1,2]:
        for k in range(len(LOH_list)):
            counts[(i,j,k)] = 0

        for line in open(filename):
            line = line.strip()
            cols = line.split(' ')
            first = int(cols[3]) 
            second = int(cols[7])
            
            for k in range(len(LOH_list)):
                (start, end) = LOH_list[k]
                if (start < first and first < end) or (start < second and second < end):
                    counts[(i,j,k)] += 1
                    break
ff = open(output_dir + '/' + CHROM + '_graph', 'w')
for (i,j,k) in counts:
    ff.write(str(i)+'\t'+str(j)+'\t'+str(k)+'\t'+str(counts[(i,j,k)])+'\n')
ff.close()



