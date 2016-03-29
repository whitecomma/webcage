import json
from pyfasta import Fasta
import os


chrom_human = map(str, range(1, 23)) + ['X', 'Y', 'M']
chrom_mouse = map(str, range(1, 20)) + ['X', 'Y', 'M']
chrom_zfish = map(str, range(1, 26)) + ['M']

model_hg19 = ['a375_1', 'hela_1', 'hl60_nonribo', 'hl60_ribo', 'hek293t_1']
model_hg38 = ['hg38_a', 'hg38_b']
model_mm9 = ['el4_1', 'mesc_1', 'rn2c_1', 'mesc_2']
model_mm10 = ['mm10_a', 'mm10_b'] 
model_dr10 = ['dr_1']

func_mdl = lambda x: lambda y: {'text':y[1], 'value':'mdl_{0}_{1}'.format(x, y[0])}

mdl_hg19 = map(func_mdl('human'), enumerate(model_hg19))
mdl_hg38 = map(func_mdl('human'), enumerate(model_hg38))
mdl_mm9 = map(func_mdl('mouse'), enumerate(model_mm9))
mdl_mm10 = map(func_mdl('mouse'), enumerate(model_mm10))
mdl_dr10 = map(func_mdl('zfish'), enumerate(model_dr10))


ref_human = ['hg19', 'hg38']
ref_mouse = ['mm9', 'mm10']
ref_zfish = ['dr10']

spec = {
    'human': {'chrom':chrom_human, 'refgem':ref_human},
    'mouse': {'chrom':chrom_mouse, 'refgem':ref_mouse},
    'zfish': {'chrom':chrom_zfish, 'refgem':ref_zfish}
}

model = {
    'hg19': mdl_hg19,
    'hg38': mdl_hg38,
    'mm9': mdl_mm9,
    'mm10': mdl_mm10,
    'dr10': mdl_dr10
}

json.dump(spec, open('spec.json', 'w'))
json.dump(model, open('model.json', 'w'))










