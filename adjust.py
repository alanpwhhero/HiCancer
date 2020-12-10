import sys

hapcut_file = sys.argv[1]
format_file = sys.argv[2]
final_file = sys.argv[3]

def reverse(cols):
    new_cols = cols
    tmp = new_cols[1]
    new_cols[1] = new_cols[2]
    new_cols[2] = tmp
    return new_cols  

blocks = []
for line in open(hapcut_file):
    line = line.strip()
    if line[0:5] == 'BLOCK':
        block = []
        
    elif line[0] == '*':
        blocks.append(block)
    else:
        cols = line.split('\t')
        cols[4] = int(cols[4])
        block.append(cols)


max_len = 0
for block in blocks:
    if len(block) > max_len:
        max_len  = len(block)
        main_block = block

phasing = {}
for cols in main_block:
    chrom = cols[3]
    pos = int(cols[4])
    allele_1 = cols[1]
    allele_2 = cols[2]
    if allele_1 in ['0', '1'] and allele_2 in ['0', '1']:
        phasing[(chrom, pos)] = (allele_1, allele_2)


segments = []
current_seg = []
for line in open(format_file):
    line = line.strip()
    if line[0:5] == 'BLOCK' or line[0] == '*':
        continue
    cols = line.split('\t')
    chrom = cols[3]
    pos = int(cols[4])
    if  (chrom, pos) in phasing:
        if len(current_seg) != 0:
            segments.append(current_seg)
        current_seg = []
        current_seg.append(cols)
    else:
        current_seg.append(cols)
  
    

if len(current_seg) != 0:
    segments.append(current_seg)

    
fo = open(final_file, 'w')
fo.write('BLOCK\n')
for i in range(len(segments)):
    seg = segments[i]
    first_chrom = seg[0][3]
    first_pos = int(seg[0][4])
    if (first_chrom, first_pos) in phasing:
        base_cols = seg[0]
    else:
        base_cols = segments[i+1][0]
    base_chrom = base_cols[3]
    base_pos = int(base_cols[4])
    base_allele_1 = base_cols[1]
    base_allele_2 = base_cols[2]

    (base_true_allele_1, base_true_allele_2) = phasing[(base_chrom, base_pos)]
    if (base_allele_1, base_allele_2) == (base_true_allele_1, base_true_allele_2):
        flag = 'same'
    elif (base_allele_1, base_allele_2) == (base_true_allele_2, base_true_allele_1):
        flag = 'oppo'
    else:
        print("ERROR")
        exit()
    if flag == 'oppo':
        for j in range(len(seg)):
            seg[j] = reverse(seg[j])
            for item in seg[j]:
                fo.write(item + '\t')
            fo.write('\n')
    else:
        for j in range(len(seg)):
            for item in seg[j]:
                fo.write(item + '\t')
            fo.write('\n')
            
fo.write('********\n')
fo.close()





