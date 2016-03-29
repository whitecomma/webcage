import subprocess
from cStringIO import StringIO
from itertools import dropwhile
import re
from pyfasta import Fasta

def CallBWA(str_fa, str_refgem, int_thrds=1):
    str_bwa = r'bwa samse {1} <(bwa aln -n 0 -t {2} {1} {0}) {0}'.format(str_fa, str_refgem, int_thrds)
    str_bwa_res = subprocess.check_output(str_bwa, shell=True, executable='/bin/bash')
    g_sam = StringIO(str_bwa_res)
    g_sgsam = FilterSam(g_sam)
    return g_sgsam

def __TestSam(lst_rc, re_pat):
    idx_flag = 1
    idx_quality = 4
    idx_cigar = 5
    if int(lst_rc[idx_quality]) < 10:
        return False
    if re_pat.search(lst_rc[idx_cigar])is not None:
        return False
    if int(lst_rc[idx_flag]) not in (0, 16):
        return False
    return True

def FilterSam(g_sam):
    g_f_psam = (line.strip().split('\t') for line in dropwhile(lambda line: line.startswith('@'), g_sam) if line.strip() != '')
    idx_idx = 0
    re_cigar = re.compile('H')
    g_psam = (lst_rc for lst_rc in g_f_psam if __TestSam(lst_rc, re_cigar) == True)
    str_prevrc = ''
    for lst_rc in g_psam:
        if lst_rc[idx_idx] == str_prevrc:
            continue
        else:
            str_prevrc = lst_rc[idx_idx]
            yield '{0}\n'.format('\t'.join(lst_rc))

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
    return ''.join(lst_rcseq)

def OrganizeSgsam(g_sgsam):
    gn_sgsam = (str_line.strip().split('\t') for str_line in g_sgsam)

    idx_sgid = 0
    idx_flag = 1
    idx_chr = 2
    idx_beg = 3
    idx_seq = 9

    str_strand = ''
    int_beg = 0
    int_end = 0
    int_csite = 0
    str_seq = ''
    for lst_sgsam in gn_sgsam:
        if lst_sgsam[idx_flag] == '16':
            str_strand = '-'
        elif lst_sgsam[idx_flag] == '0':
            str_strand = '+'
        if str_strand == '+':
            str_seq = lst_sgsam[idx_seq]
            int_beg = int(lst_sgsam[idx_beg])
            int_end = int(lst_sgsam[idx_beg]) - 1 + len(str_seq)
            int_csite = int_end - 5
        elif str_strand == '-':
            str_seq = __SeqRc(lst_sgsam[idx_seq])
            int_end = int(lst_sgsam[idx_beg])
            int_beg = int(lst_sgsam[idx_beg]) - 1 + len(str_seq)
            int_csite = int_end + 5
        lst_psg = [lst_sgsam[idx_sgid], lst_sgsam[idx_chr]]
        lst_psg.append(str_strand)
        lst_psg.append(str(int_beg))
        lst_psg.append(str(int_end))
        lst_psg.append(str_seq)
        lst_psg.append(str(int_csite))
        yield '{0}\n'.format('\t'.join(lst_psg))

def __ParseSeq(str_chr, int_beg, int_end, str_strand, fa_ref, re_pat):
    str_seq = fa_ref.sequence({'chr':str_chr, 'start':int_beg, 'stop':int_end, 'strand':str_strand}).upper()
    lst_pam = [range(re_obj.start(), re_obj.end()-1) for re_obj in re_pat.finditer(str_seq)]
    lst_pamcord = reduce(lambda x,y: x+y, lst_pam)
    lst_sg = []
    int_sgbeg = 0
    int_sgend = 0
    for idx in lst_pamcord:
        if str_strand == '+':
            int_sgbeg = int_beg + idx - 21
            int_sgend = int_beg + idx + 1
        elif str_strand == '-':
            int_sgbeg = int_end - idx - 1
            int_sgend = int_end - idx + 21

        str_sg = fa_ref.sequence({'chr':str_chr, 'start':int_sgbeg, 'stop':int_sgend, 'strand':str_strand}).upper()
        yield str(str_sg)

def ExtractSg(str_refgem, str_chr, int_beg, int_end, str_drct):
    fa_ref = Fasta(str_refgem)
    re_pat = re.compile('G+')
    gn_f_sg = __ParseSeq(str_chr, int_beg, int_end, '+', fa_ref, re_pat)
    gn_r_sg = __ParseSeq(str_chr, int_beg, int_end, '-', fa_ref, re_pat)
    if str_drct == 'f':
        for str_sg in gn_f_sg:
            yield str_sg
    elif str_drct == 'r':
        for str_sg in gn_r_sg:
            yield str_sg
    elif str_drct == 'b':
        for str_sg in gn_f_sg:
            yield str_sg
        for str_sg in gn_r_sg:
            yield str_sg


def Sg2Fa(gn_sg):
    for i, str_sg in enumerate(gn_sg):
        str_id = '>sg%d'% (i+1)
        yield '{0}\n{1}\n'.format(str_id, str_sg)