import os
import seq

s1 = '{0}/hg19.fa'.format(os.environ['BWADB'])
f1 = '{0}/hg19.fa'.format(os.environ['FASTADB'])
fa = seq.s


from sgpocessor import *
from seqeval import *


# g1 = CallBWA(fa, s1)
# g2 = FilterSam(g1)
# g3 = OrganizeSgsam(g2)
# res = FeatureEval(g3, 'nmeth3015.pkl', f1)


a = ExtractSg(f1, 'chr3', 195609062, 195609284, 'b')
b = Sg2Fa(a)
c = ''.join(b)
g1 = CallBWA(c, s1)
g2 = FilterSam(g1)
g3 = OrganizeSgsam(g2)
res = FeatureEval(g3, 'nmeth3015.pkl', f1)
