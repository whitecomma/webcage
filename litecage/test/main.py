from sgpocessor import *
from seqeval import *
import sys
import os

s1 = '{0}/hg19.fa'.format(os.environ['BWADB'])
f1 = '{0}/hg19.fa'.format(os.environ['FASTADB'])


g1 = CallBWA(sys.argv[1], s1)
g2 = FilterSam(g1)
g3 = OrganizeSgsam(g2)
res = FeatureEval(g3, 'nmeth3015.pkl', f1)

sys.stdout.write(''.join(res))
