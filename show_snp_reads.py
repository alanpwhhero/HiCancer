import pysam
import sys
bam_file = sys.argv[1]
snp_file = sys.argv[2]
out_file = sys.argv[3]

def pile_up_snp_reads(samfile, chrom, target_pos, ref_base, alt_base):
    target_pos -= 1
    out = {}
    out[ref_base] = []
    out[alt_base] = []
    for pileupcolumn in samfile.pileup(chrom, target_pos, target_pos + 1):
        if pileupcolumn.pos != target_pos:
            continue
        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                base = pileupread.alignment.query_sequence[pileupread.query_position]
                if base != ref_base and base != alt_base:
                    continue
                out[base].append(pileupread.alignment.query_name)
    return out


samfile = pysam.AlignmentFile(bam_file, 'rb')




fo = open(out_file, 'w')
# read snps
num = 0
for line in open(snp_file):
    if num % 1000 == 0:
        print(num)
    num += 1
    if line[0] == '#':
        continue
    line = line.strip()
    cols = line.split()
    chrom = cols[0]
    pos = int(cols[1])
    ref_base = cols[3]
    alt_base = cols[4]
    if len(ref_base) > 1 or len(alt_base) > 1:
        continue
    piledupreads1snp = pile_up_snp_reads(samfile, chrom, pos, ref_base, alt_base)
    
    fo.write(chrom + '\t' + str(pos) + '\t' + ref_base + '\t' + str(len(piledupreads1snp[ref_base]))
             + '\t' + alt_base + '\t' + str(len(piledupreads1snp[alt_base])) + '\t')
    for i in range(len(piledupreads1snp[ref_base])-1):
        fo.write(piledupreads1snp[ref_base][i]+" ")
    if len(piledupreads1snp[ref_base]) > 0:
        fo.write(piledupreads1snp[ref_base][len(piledupreads1snp[ref_base])-1])
    fo.write('\t')
    for i in range(len(piledupreads1snp[alt_base])-1):
        fo.write(piledupreads1snp[alt_base][i]+" ")
    if len(piledupreads1snp[alt_base]) > 0:
        fo.write(piledupreads1snp[alt_base][len(piledupreads1snp[alt_base])-1])
    fo.write('\n')
  

samfile.close()

