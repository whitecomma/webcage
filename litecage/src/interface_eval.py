import os
import sys
from sgpocessor import *
from seqeval import *
import tempfile
import uuid

def SgEval(opts):
    str_path_mdl = opts.sfunc
    str_ref_bwa = '{0}/{1}.fa'.format(os.environ['BWADB'], opts.ref)
    str_ref_fasta = '{0}/{1}.fa'.format(os.environ['FASTADB'], opts.ref)
    int_thrd = opts.thrd
    str_fa = ''
    ft = tempfile.NamedTemporaryFile('w+t', suffix='.sgfa', prefix=str(uuid.uuid4()), dir='/tmp')
    if opts.fa is not None:
        str_fa = opts.fa
    else:
        dict_drct = {'two-sided': 'b', 'pos': 'f', 'neg': 'r'}
        gn_sg = ExtractSg(str_ref_fasta, opts.chrom, opts.beg, opts.end, dict_drct[opts.drct])
        gn_fa = Sg2Fa(gn_sg)
        for fa in gn_fa:
            ft.write(fa)
        ft.seek(0)
        str_fa = ft.name
    g_sam = CallBWA(str_fa, str_ref_bwa, int_thrd)
    ft.close()
    g_sgsam = FilterSam(g_sam)
    g_sg = OrganizeSgsam(g_sgsam)
    lst_res = FeatureEval(g_sg, str_path_mdl, str_ref_fasta)
    sys.stdout.write(''.join(lst_res))

        


