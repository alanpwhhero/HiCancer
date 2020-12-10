import operator
import sys

def read_file(CN_file):
    blocks = []
    for line in open(CN_file):
        line = line.strip()
        if line[0:5] == 'BLOCK':
            block = []
            continue
        if line[0] == '*':
            blocks.append(block)
            continue
        cols = line.split('\t') 
        cols[4] = int(cols[4])
        block.append(cols)
    return blocks

def Greater(block, k): 
    n = len(block)
    l = 0 
    r = n - 1 
  
    # Stores the index of the left most element 
    # from the array which is greater than k 
    leftGreater = n 
    # Finds number of elements greater than k 
    while (l <= r): 
        m = int(l + (r - l) / 2)  
        # If mid element is greater than 
        # k update leftGreater and r 
        if (int(block[m][4]) > k): 
            leftGreater = m 
            r = m - 1 
  
        # If mid element is less than 
        # or equal to k update l 
        else: 
            l = m + 1 
  
    # Return the count of elements  
    # greater than k 
    return leftGreater 


def find_nearest_snps(block_1, pos, first_index, num_of_nearest_snp):
    if first_index == 0:
            
        left = 0
        right = num_of_nearest_snp - 1
    elif first_index == len(block_1):
        right = len(block_1) - 1
        left = right - num_of_nearest_snp + 1

    else:
        left = first_index - 1
        right = first_index
        
        while right - left + 1 < 5:
            if left == 0:
                right = num_of_nearest_snp - 1
                break
            if right ==  len(block_1) - 1:
                left = right - num_of_nearest_snp + 1
                break
            if abs(int(block_1[left][4]) - pos) < abs(int(block_1[right][4]) - pos):
                left -= 1
            else: 
                right += 1    
 

    return (left, right)

def reverse(cols):
    new_cols = cols
    tmp = new_cols[1]
    new_cols[1] = new_cols[2]
    new_cols[2] = tmp
    tmp = new_cols[12]
    new_cols[12] = new_cols[13]
    new_cols[13] = tmp
    return new_cols  
    

def merge_blocks(block_1, block_2, flag):
    block_merged = []
    i = 0
    j = 0

    while i < len(block_1) and j < len(block_2):
        pos_i = int(block_1[i][4])
        pos_j = int(block_2[j][4])
        if pos_i < pos_j:
            block_merged.append(block_1[i])
            i += 1
        else:
            if flag == 'same':
                new_line = block_2[j]
            else:
                new_line = reverse(block_2[j])
            block_merged.append(new_line)
            j += 1
    if i == len(block_1):
        for k in range(j, len(block_2)):
            if flag == 'same':
                new_line = block_2[k]
            else:
                new_line = reverse(block_2[k])
            block_merged.append(new_line)
        return block_merged
    if j == len(block_2):
        for k in range(i, len(block_1)):
            block_merged.append(block_1[k])
        return block_merged

def merge(block_1, block_2):
    num_same_snp = 0
    num_oppo_snp = 0
    num_dismatch_snp = 0
    for i in range(len(block_2)):
        pos = int(block_2[i][4])
        first_index = Greater(block_1, pos)
        left, right = find_nearest_snps(block_1, pos, first_index, 5)
         
        if abs(int(block_1[left][4]) - pos) > 1000000 or abs(int(block_1[right][4]) - pos) > 1000000:
            continue
        cn_2_a = block_2[i][12]
        cn_2_b = block_2[i][13]
        num = right - left + 1
        num_same = 0
        num_oppo = 0 
        num_dismatch = 0
        for j in range(left, right + 1):
            cn_1_a = block_1[j][12]
            cn_1_b = block_1[j][13]
            if cn_2_a == cn_1_a and cn_2_b == cn_1_b:
                num_same += 1
            elif cn_2_a == cn_1_b and cn_2_b == cn_1_a:
                num_oppo += 1
            else:
                num_dismatch += 1
        if num_same * 1.0 / num >= 0.6:
            if cn_2_a == cn_2_b:
                continue
            num_same_snp += 1
        elif num_oppo * 1.0 / num >= 0.6:
            if cn_2_a == cn_2_b:
                continue
            num_oppo_snp += 1
        else:
            num_dismatch_snp += 1
    num_total_test = num_same_snp + num_oppo_snp + num_dismatch_snp
    if num_total_test < 10 and num_total_test < len(block_2) * 0.5:
        return 'False'
    if num_same_snp / num_total_test > 0.8: 
        return 'same'
    elif  num_oppo_snp / num_total_test > 0.8:
        return 'oppo'
    else:
        return 'False'


def merge_all(max_block, blocks, removed_block_index):
    block_merged = max_block
    for i in removed_block_index:
        flag = removed_block_index[i]
        block = blocks[i]
        for cols in block:
            if flag == 'same':
                newline = cols
            else:
                newline = reverse(cols)
            block_merged.append(newline)
    block_merged_sorted = sorted(block_merged, key = lambda x: x[4]) 
    return block_merged_sorted

def method_1(blocks):


    large_size_index = set([])
    
    for i in range(len(blocks)):
        block = blocks[i]
        block_size = len(block)
        if block_size > 100:
            large_size_index.add(i)
            

    new_big_blocks = {}
    removed_block_index = set([])
    for index in large_size_index:
        big_block = blocks[index]
        flag_dict = {}
        for i in range(len(blocks)):
            if i in large_size_index:
                continue
            if i in removed_block_index:
                continue
            flag = merge(big_block, blocks[i])

            if flag == 'False':
                continue

            removed_block_index.add(i)
            flag_dict[i] = flag

        big_block = merge_all(big_block, blocks, flag_dict)
        new_big_blocks[index] = big_block



    new_blocks = []
    for i in range(len(blocks)): 
        if i in large_size_index:
            new_blocks.append(new_big_blocks[i])
            continue
        if i in removed_block_index:
            continue
        new_blocks.append(blocks[i])
    
    return new_blocks


def check_match(block_1, block_2):
    CN_counts_1 = {}
    for cols in block_1:
        cn_left = int(cols[12])
        cn_right = int(cols[13])
        if (cn_left, cn_right) not in CN_counts_1:
            CN_counts_1[(cn_left, cn_right)] = 0
        CN_counts_1[(cn_left, cn_right)] += 1


    CN_counts_2 = {}
    for cols in block_2:
        cn_left = int(cols[12])
        cn_right = int(cols[13])
        if (cn_left, cn_right) not in CN_counts_2:
            CN_counts_2[(cn_left, cn_right)] = 0
        CN_counts_2[(cn_left, cn_right)] += 1
   
    max_CN_1 = max(CN_counts_1.items(), key=operator.itemgetter(1))[0]    
    max_CN_2 = max(CN_counts_2.items(), key=operator.itemgetter(1))[0]    
    if max_CN_1[0] == max_CN_1[1]:
        return 'False'
    if max_CN_2[0] == max_CN_2[1]:
        return 'False'
    if CN_counts_1[max_CN_1] < len(block_1) * 0.8:
        return 'False'
    if CN_counts_2[max_CN_2] < len(block_2) * 0.8:
        return 'False'
    if max_CN_1[0] == max_CN_2[0] and max_CN_1[1] == max_CN_2[1]:
        return 'same'
    if max_CN_1[0] == max_CN_2[1] and max_CN_1[1] == max_CN_2[0]:
        return 'oppo'
  
    return 'False'

def get_median(block):
    return int(block[int(len(block)/2)][4])

def merge_pairwise(block_1, block_2):
    block_1_head = block_1[:20]
    block_1_tail = block_1[len(block_1)-20:]
    block_2_head = block_2[:20]
    block_2_tail = block_2[len(block_2)-20:]

    median_1_head = get_median(block_1_head)
    median_1_tail = get_median(block_1_tail)
    median_2_head = get_median(block_2_head)
    median_2_tail = get_median(block_2_tail)

    if median_1_tail < median_2_head and abs(median_1_tail - median_2_head) < 10000000:
        return check_match(block_1_tail, block_2_head)
    if median_2_tail < median_1_head and abs(median_2_tail - median_1_head) < 10000000:
        return check_match(block_2_tail, block_1_head)

    return 'False'

def reverse_flag(flag):
    if flag == 'same':
        return 'oppo'
    if flag == 'oppo':
        return 'same'

def merge_by_guide(info, blocks):
    block_merged = []
    for (i, flag, root) in info:
        block = blocks[i]
        for cols in block:
            if flag == 'same':
                newline = cols
            else:
                newline = reverse(cols)
            block_merged.append(newline)
    block_merged_sorted = sorted(block_merged, key = lambda x: x[4]) 
    return block_merged_sorted

def method_2(blocks):
    guide = {}
    for i in range(len(blocks)-1):
        for j in range(i + 1, len(blocks)):
            if j in guide:
                continue
            flag = merge_pairwise(blocks[i], blocks[j]) 
            if flag == 'False':
                continue
            if i not in guide:
                guide[i] = ('same', i)
                 
            (flag_i, root) = guide[i]
         
            if flag == 'same':
                guide[j] = (flag_i, root)
            else:
                flag_j = reverse_flag(flag_i)
                guide[j] = (flag_j, root)

    guide_tree = {}
    for i in guide:
        (flag, root) = guide[i]
        if root not in guide_tree:
            guide_tree[root] = []
        guide_tree[root].append((i, flag, root))

    merged_blocks = {}
    for root in guide_tree:
        merged_blocks[root] = merge_by_guide(guide_tree[root], blocks)

    new_blocks = []
    for i in range(len(blocks)): 
        if i in merged_blocks:
            new_blocks.append(merged_blocks[i])
            continue
        if i in guide:
            continue
        new_blocks.append(blocks[i])
    
    return new_blocks

def remove_1(blocks):
    large_size_index = set([])
    
    for i in range(len(blocks)):
        block = blocks[i]
        block_size = len(block)
        if block_size > 100:
            large_size_index.add(i)
            

    removed_block_index = set([])
    for index in large_size_index:
        big_block = blocks[index]
        for i in range(len(blocks)):
            if i in large_size_index:
                continue
            if i in removed_block_index:
                continue
            start = int(big_block[3][4])    
            end = int(big_block[len(big_block)-3][4])
            p1 = Greater(blocks[i], start)
            p2 = Greater(blocks[i], end)
            ratio = (p2 - p1) * 1.0 / len(blocks[i])
            if ratio > 0.9:
                removed_block_index.add(i) 
            
    new_blocks = []
    for i in range(len(blocks)): 
        if i in removed_block_index:
            continue
        new_blocks.append(blocks[i])
    
    return new_blocks
 

def remove_2(blocks):
    new_blocks = []
    for block in blocks:
        if len(block) >= 100:
            new_blocks.append(block)
    return new_blocks


def write_file(blocks, new_CN_file):
    fo = open(new_CN_file, 'w')
    for block in blocks:
        fo.write('BLOCK\n')
        for cols in block:
            for i in range(len(cols) - 1):
                fo.write(str(cols[i]) + '\t')
            fo.write(cols[len(cols)-1] + '\n')
        fo.write('********\n')
    fo.close()

def phase2(CN_file, new_CN_file):
    blocks = read_file(CN_file)

    blocks = method_1(blocks)
    blocks = remove_1(blocks)
    blocks = method_2(blocks)
    blocks = remove_2(blocks)
    write_file(blocks, new_CN_file)

infile = sys.argv[1]
outfile = sys.argv[2]
phase2(infile, outfile)

