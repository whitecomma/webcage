#! /bin/bash

bwadb=$1
fa=$2

#fa=">sg1\nTGGGGCTGGATAATGGAGCGTGG\n>sg2\nCGGTCCAACAACGATCCCAGAGG\n"

bwa samse $bwadb/hg19.fa <(echo -e "$fa" | bwa aln -n 0 $BWADB/hg19.fa - ) <(echo -e "$fa")
