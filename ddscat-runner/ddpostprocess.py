from glob import glob
import os
import os.path
import shutil
import subprocess
import sys

from argparse import ArgumentParser

def pad_number(num):
    length = len(str(num))
    return ((3 - length) * '0') + str(num)

ddpost_par = """
'{e_file}'            = name of file with E stored
'{outfile}'                  = prefix for name of VTR output files
{e_e2}   = IVTR (set to 1 to create VTR output)
0   = ILINE (set to 1 to evaluate E along a line)
"""


def main():
    argparser = ArgumentParser()
    argparser.add_argument('subdir')
    args = argparser.parse_args()

    os.chdir(args.subdir)
    subprocess.call('mkdir vtr', shell=True)
    subprocess.call('cp ~/scratch/exec/ddpostprocess .', shell=True)

    vtrdir = os.path.join(args.subdir, 'vtr')

    efiles = glob('w*r000k000.E1')
    efiles.sort()
    i = 0
    for i, efile in enumerate(efiles):
        with open('ddpostprocess.par', 'w') as fp:
            fp.write(ddpost_par.format(
                e_file=efile,
                outfile='vtr/wav_{}'.format(i),
                e_e2='1'
            ))

        subprocess.call('./ddpostprocess', shell=True)
        subprocess.call('rm ddpostprocess.par', shell=True)

    unchanged = glob('vtr/*')

    for file in unchanged:
        newfile = file.replace('_1.vtr', '.vtr')
        shutil.move(file, newfile)

    os.chdir('..')
    shutil.move(vtrdir, '{}_vtr'.format(args.subdir))

if __name__ == "__main__":
    main()
