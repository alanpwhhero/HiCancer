# HiCancer


Description 

HiCancer is a pipeline for phasing cancer genome. It uses Hi-C paired-end reads and called SNPs as input and outputs chromosome-level haplotypes of cancer genome. HiCancer filtered somatic SNPs and phase the LOH regions in a correct way. At the same time, HiCancertakes advantage of allelic copy number imbalance in aneuploid regions and linkage disequilibrium information to improve thecompleteness and accuracy by assembling fragmented haplotypes, adding the lost SNPs back into haplotypes (imputation)and correcting the switching errors.



Dependency 

1. python
The majoy part of HiCancer is written in Python, so Python has to be installed. Python2.7(or above) is suggested.
2. samtools
https://github.com/samtools/samtools
3. bwa
http://bio-bwa.sourceforge.net/
4. HapCUT2
https://github.com/vibansal/HapCUT2
5. Beagle5
http://faculty.washington.edu/browning/beagle/beagle.html
Also need to download the genetic map files as beagle input
6. reference genome
http://hgdownload.soe.ucsc.edu/downloads.html#human
7. 1000 genomic project vcf files
https://www.internationalgenome.org/data



Usage 

The whole pipeline is contained in HiCancer.sh. The users need to fill the first part ("input files") of HiCancer.sh which represent the all input files and parameters needed, and then run it. 



Output 

hapcutfile_filtered_beagleoutput_*.final gives the phased *th chromosme before completing step.
The result of completing step is contained in chr*_phasing files. 
 


