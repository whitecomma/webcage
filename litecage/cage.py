import argparse
import os
import sys
import src.ui_eval as ui

def main():
    
    str_prog = 'CAGE'
    str_usage = 'python cage.py <command> [options]'
    str_desc = r'''
CRISPR KO Analysis based on Genomic Editing data
Version: 1.0.0
------------------------------------------------
A CRISPR-cas9 based Genome Editing data analysis pipeline, 
for the analysis of indels and microhomology patterns from 
CRISPR-Cas9 Knock-Out NGS data.
'''
    p = argparse.ArgumentParser(prog=str_prog,
                                 usage=str_usage,
                                 description=str_desc,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

    sp = p.add_subparsers(title='Command', metavar='')

    p_ev = sp.add_parser('eval',
                         description='sgRNA KO efficiency evaluation',
                         usage='python cage.py eval [options]',
                         help='sgRNA KO efficiency evaluation')
    ui.ParseEval(p_ev)

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'eval':
            p_ev.print_help()
        else:
            p.print_help()
        sys.exit(1)

    if 'BWADB' not in os.environ:
        p.error('$BWADB Not Exist. See README')
    
    if 'FASTADB' not in os.environ:
        p.error('$FASTADB Not Exist. See README')
    
    opts = p.parse_args()

    if sys.argv[1] == 'eval':
        import src.interface_eval as eval
        eval.SgEval(opts)
        

if __name__ == '__main__':
    main()
