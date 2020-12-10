#input files
ref= #e.g./hive/weihuap/data/human_genome/hg19/hg19.fa
read1= #e.g. SRR6251264_1.fastq
read2= #e.g. SRR6251264_2.fastq
g1000file= #vcf file, download from 1000 genomic project website
snpfile= #input SNPs called
beagle= #beagle jar file 
mapprefix= #directory of genetic map files from beagle website
numthreads=48
outputdir= #output directory

#other variables
samfile=${outputdir}/all.sam
bamfile=${outputdir}/all.bam
bamfilesrted=${outputdir}/all_sorted.bam
samfile1=${outputdir}/read1.sam
samfile2=${outputdir}/read2.sam
snpfile1=${outputdir}/snpfile1.txt
snpfile2=${outputdir}/snpfile2.txt
ratiofile=${outputdir}/LOH_ratio.txt
LOH_regions=${outputdir}/LOH_regions.txt
readsmapped=${outputdir}/all.readsmapped
hapcutfrgmt=${outputdir}/fragment
hapcutfile=${outputdir}/hapcutfile

#alignment process
bwa mem -t $numthreads $ref $read1 $read2 > $samfile
samtools view -S -b $samfile > $bamfile
samtools sort -@ $numthreads -o $bamfilesrted $bamfile
samtools index -b $bamfilesrted

bwa mem -t $numthreads $ref $read1 > $samfile1
bwa mem -t $numthreads $ref $read2 > $samfile2

# pre-process
python 1000g_filter.py $g1000file $snpfile $snpfile1
python filter_only1.py $snpfile1 $snpfile2
python LOH.py $snpfile2 $ratiofile
python get_LOH.py $ratiofile $LOH_regions
python show_snp_reads.py $bamfilesrted $snpfile2 $readsmapped

#run HapCut2
extractHAIRS --hic 1 --bam $bamfilesrted --VCF $snpfile2 --out $hapcutfrgmt --indels 1
HAPCUT2 --hic 1 --fragments $hapcutfrgmt --VCF $snpfile2 --output $hapcutfile

#pos-process
python phase.py $hapcutfile ${hapcutfile}_1 #(optional)
python remove_LOH_var.py $LOH_regions $hapcutfile ${hapcutfile}_filtered

#run Beagle

hapcutfile=${hapcutfile}_filtered
beagleinput=${hapcutfile}_beagleinput
beagleoutput=${hapcutfile}_beagleoutput
python split_cn_file.py $hapcutfile
for i in {1..22}
do
python get_input_beagle.py ${hapcutfile}_${i} ${snpfile2}_${i} $snp_file ${beagleinput}_${i}
java -Xmx200g -jar $beagle ref=${g1000file}_${i}  gt=${beagleinput}_${i} out=${beagleoutput}_${i} map=${mapprefix}/plink.chr${i}.GRCh37.map impute=false nthreads=${numthreads}
gunzip ${beagleoutput}_${i}
python change_format.py ${beagleoutput}_${i} ${beagleoutput}_${i}.format
python adjust.py ${hapcutfile}_${i} ${beagleoutput}_${i}.format ${beagleoutput}_${i}.final

done

#completing

for c in {1..22}
do
CHROM=str${c}
python select_.py $CHROM $samfile1
python select_.py $CHROM $samfile2
samtools view -q 10 ${samfile1}_${CHROM}  | awk '{ print $2" "$3" "$4" "0" "$5" "$6" "$10" "$1  }' > ${CHROM}_read1.txt
samtools view -q 10 ${samfile2}_${CHROM}  | awk '{ print $2" "$3" "$4" "0" "$5" "$6" "$10" "$1  }' > ${CHROM}_read2.txt

grep ${CHROM} $readsmapped > ${readsmapped}_${CHROM}

file="hg19_sizes"
while IFS=$'\t' read -r f1 f2
do
    if [ $f1 == $CHROM ]
    then
        chrlen=$f2
    fi
done < "$file"

python get_segments.py ${CHROM} ${chrlen} ${beagleoutput}_${i}.final $outputdir

LOH_num=0
nonLOH_num=0
file=${outputdir}_${CHROM}_LOH_nonLOH_regions
while IFS=$'\t' read -r f1 f2 f3
do
    if [ $f3 == 'LOH' ]
    then
        LOH_num=$((LOH_num+1))
    else
        nonLOH_num=$((nonLOH_num+1))
    fi
done < "$file"

python get_LOH_2_nonLOH.py $CHROM $outputdir 
python LOH_phasing.py $CHROM $outputdir
done


