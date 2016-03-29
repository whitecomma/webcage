import numpy as np
import pandas as pd
from cStringIO import StringIO
from pyfasta import Fasta
from sklearn.externals import joblib

def LoadModel(str_of_md):
    return joblib.load(str_of_md)

def LassoEval(model, x, columns):
    return model.predict(x[:,columns]).ravel()

def LogitEval(model, x, columns):
    return model.predict_proba(x[:,columns])[:,1].ravel()

def __SeqRc(str_seq):
    lst_rcseq = [c for c in str_seq[::-1]]
    for i in xrange(len(lst_rcseq)):
        if lst_rcseq[i] == 'A':
            lst_rcseq[i] = 'T'
        elif lst_rcseq[i] == 'T':
            lst_rcseq[i] = 'A'
        elif lst_rcseq[i] == 'C':
            lst_rcseq[i] = 'G'
        elif lst_rcseq[i] == 'G':
            lst_rcseq[i] = 'C'
        elif lst_rcseq[i] == 'N':
            lst_rcseq[i] = 'N'
    return ''.join(lst_rcseq)

def __EncodeSeq(str_seq, dict_code):
    lst_code = []
    for c in str_seq:
        lst_code.extend(dict_code[c])
    return lst_code

def __FormulateFeature(lst_sg, fa_ref, dict_code, int_ups, int_dws):
    idx_sgid = 0
    idx_chr = 1
    idx_strand = 2
    idx_beg = 3
    idx_end = 4
    idx_seq = 5

    lst_seq = [lst_sg[idx_sgid]]
    str_ups =''
    str_dws = ''

    if lst_sg[idx_strand] == '-':
        int_bups = int(lst_sg[idx_beg]) + int_ups
        int_eups = int(lst_sg[idx_beg]) + 1
        str_ups = fa_ref[lst_sg[idx_chr]][int_eups - 1:int_bups].upper()
        str_ups = __SeqRc(str_ups)
        int_bdws = int(lst_sg[idx_end]) - 1
        int_edws = int(lst_sg[idx_end]) - int_dws
        str_dws = fa_ref[lst_sg[idx_chr]][int_edws - 1:int_bdws].upper()
        str_dws = __SeqRc(str_dws)
    else:
        int_bups = int(lst_sg[idx_beg]) - int_ups
        int_eups = int(lst_sg[idx_beg]) - 1
        str_ups = fa_ref[lst_sg[idx_chr]][int_bups - 1:int_eups].upper()
        int_bdws = int(lst_sg[idx_end]) + 1
        int_edws = int(lst_sg[idx_end]) + int_dws
        str_dws = fa_ref[lst_sg[idx_chr]][int_bdws - 1:int_edws].upper()
    lst_seq.extend(__EncodeSeq(str_ups, dict_code))
    lst_seq.extend(__EncodeSeq(lst_sg[idx_seq], dict_code))
    lst_seq.extend(__EncodeSeq(str_dws, dict_code))
    return lst_seq



def ExtractSeqFeature(g_sg, str_refgem, int_ups, int_dws):
    gn_sg = (str_sg.strip().split('\t') for str_sg in g_sg if str_sg.strip() != '')
    strio_seq = StringIO()

    fa_ref = Fasta(str_refgem)
    dict_code = dict(N=['0','0','0','0'], A=['1','0','0','0'], C=['0','1','0','0'], G=['0','0','1','0'], T=['0','0','0','1'])
    lst_code = ['A', 'C', 'G', 'T']
    lst_seq = []
    lst_header = ['sgID']
    lst_header.extend(['ups_%d_%s'% (i, j) for i in range(int_ups, 0, -1) for j in lst_code])
    lst_header.extend(['spa_%d_%s'% (i, j) for i in range(1, 21) for j in lst_code])
    lst_header.extend(['pam_%d_%s'% (i, j) for i in range(1, 4) for j in lst_code])
    lst_header.extend(['dws_%d_%s'% (i, j) for i in range(1, int_dws+1) for j in lst_code])
    for lst_sg in gn_sg:
        lst_seq = __FormulateFeature(lst_sg, fa_ref, dict_code, int_ups, int_dws)
        strio_seq.write('\t'.join(lst_seq) + '\n')
    dfm_seq = pd.read_csv(StringIO(strio_seq.getvalue()), header=None, sep='\t', index_col=None)
    dfm_seq.columns = lst_header
    strio_seq.close()
    return dfm_seq


def FeatureEval(g_sg, str_f_md, str_refgem):
    lst_sg = list(g_sg)
    mdl = LoadModel(str_f_md)
    dfm = ExtractSeqFeature(lst_sg, str_refgem, mdl['ups'], mdl['dws'])

    x = np.array(dfm.ix[:,1:], dtype=np.double)
    y = None
    if mdl['med'] == 'lasso':
        y = LassoEval(mdl['model'], x, mdl['idx'])
    elif mdl['med'] == 'logit':
        y = LogitEval(mdl['model'], x, mdl['idx'])
    dfm['score'] = y
    dfm_y = dfm[[0,-1]]

    strio_sg = StringIO()
    for line in lst_sg:
        strio_sg.write(line)
    dfm_sg = pd.read_csv(StringIO(strio_sg.getvalue()), header=None, sep='\t', index_col=None)
    dfm_sg.columns = ['sgID', 'chrom', 'strand', 'sbeg', 'send', 'qseq', 'c_site']
    strio_sg.close()

    dfm = pd.merge(dfm_sg, dfm_y, on='sgID')
    dfm.drop('c_site', axis=1, inplace=True)
    dfm.sort_values(by=['score'], ascending=False, inplace=True)
    lst_res = map(lambda s: '{0}\n'.format('\t'.join(map(str, s))),dfm.values.tolist())
    return lst_res






