from __future__ import print_function

import os
import os.path
import sys
import time
import pickle
import argparse
import shutil
import subprocess

ddscat_pbs = """
#PBS -N {subdir}

#PBS -M tgog@umich.edu
#PBS -m abe
#PBS -t 0-{max_sub}

#PBS -l procs=1
#PBS -l mem=6000MB
#PBS -l walltime=7:00:00
#PBS -V

#PBS -A kopelman_flux
#PBS -q flux
#PBS -l qos=flux

cd /scratch/kopelman_flux/tgog
cd {subdir}

python3 ../scripts/map.py $PBS_ARRAYID
"""

reduce_pbs = """
#PBS -N {subdir}

#PBS -M tgog@umich.edu
#PBS -m abe

#PBS -l procs=2
#PBS -l mem=1200MB
#PBS -l walltime=00:05:00
#PBS -V

#PBS -A kopelman_flux
#PBS -q flux
#PBS -l qos=flux

cd /scratch/kopelman_flux/tgog
cd {subdir}

python3 ../scripts/reduce.py {num_procs}
"""

ddscat_par = """
' ========== Parameter file for v7.3 ==================='
'**** Preliminaries ****'
'NOTORQ' = CMDTRQ*6 (DOTORQ, NOTORQ) -- either do or skip torque calculations
'PBCGS2' = CMDSOL*6 (PBCGS2, PBCGST, GPBICG, QMRCCG, PETRKP) -- CCG method
'GPFAFT' = CMETHD*6 (GPFAFT, FFTMKL) -- FFT method
'GKDLDR' = CALPHA*6 (GKDLDR, LATTDR, FLTRCD) -- DDA method
'NOTBIN' = CBINFLAG (NOTBIN, ORIBIN, ALLBIN) -- binary output?
'**** Initial Memory Allocation ****'
150 250 150 = dimensioning allowance for target generation
'**** Target Geometry and Composition ****'
FROM_FILE = CSHAPE*9 shape directive
0
1         = NCOMP = number of dielectric materials
'Au_evap' = file with refractive index gold
'**** Additional Nearfield calculation? ****'
1 = NRFLD (=0 to skip nearfield calc., =1 to calculate nearfield E)
1.0 1.0 1.0 1.0 1.0 1.0 (fract. extens. of calc. vol. in -x,+x,-y,+y,-z,+z)
'**** Error Tolerance ****'
1.00e-5 = TOL = MAX ALLOWED (NORM OF |G>=AC|E>-ACA|X>)/(NORM OF AC|E>)
'**** Maximum number of iterations ****'
2500     = MXITER
'**** Integration limiter for PBC calculations ****'
1.00e-2 = GAMMA (1e-2 is normal, 3e-3 for greater accuracy)
'**** Angular resolution for calculation of <cos>, etc. ****'
0.5    = ETASCA (number of angles is proportional to [(3+x)/ETASCA]^2 )
'**** Wavelengths (micron) ****'
{start_wave} {end_wave} {num_wave} 'LIN' = wavelengths (1st,last,howmany,how=LIN,INV,LOG,TAB)
'**** Refractive index of ambient medium ****'
1.3300 = NAMBIENT
'**** Effective Radii (micron) **** '
{aeff} {aeff} 1 'LIN' = eff. radii (1st,last,howmany,how=LIN,INV,LOG,TAB)
'**** Define Incident Polarizations ****'
(0,0) (1.,0.) (0.,0.) = Polarization state e01 (k along x axis)
2 = IORTH  (=1 to do only pol. state e01; =2 to also do orth. pol. state)
'**** Specify which output files to write ****'
0 = IWRKSC (=0 to suppress, =1 to write ".sca" file for each target orient.
'**** Specify Target Rotations ****'
0.    0.   1  = BETAMI, BETAMX, NBETA  (beta=rotation around a1)
0.    0.   1  = THETMI, THETMX, NTHETA (theta=angle between a1 and k)
0.    0.   1  = PHIMIN, PHIMAX, NPHI (phi=rotation angle of a1 around k)
'**** Specify first IWAV, IRAD, IORI (normally 0 0 0) ****'
0   0   0    = first IWAV, first IRAD, first IORI (0 0 0 to begin fresh)
'**** Select Elements of S_ij Matrix to Print ****'
6    = NSMELTS = number of elements of S_ij to print (not more than 9)
11 12 21 22 31 41    = indices ij of elements to print
'**** Specify Scattered Directions ****'
'LFRAME' = CMDFRM (LFRAME, TFRAME for Lab Frame or Target Frame)
1 = NPLANES = number of scattering planes
0.  0. 180. 10 = phi, theta_min, theta_max (deg) for plane A
"""


def ddscat_split(wave_range, aeff):
    proc_num, wave_start, wave_end = wave_range

    current_path = os.getcwd()
    new_folder = os.path.join(current_path, 'wavelengths_{}/'.format(proc_num))

    subprocess.call('mkdir {}'.format(new_folder), shell=True)
    subprocess.call('cp ddscat {}'.format(new_folder), shell=True)
    subprocess.call('cp shape.dat {}'.format(new_folder), shell=True)
    subprocess.call('cp Au_evap {}'.format(new_folder), shell=True)

    os.chdir(new_folder)

    wave_num = wave_end - wave_start + 1

    with open('ddscat.par', 'w') as parfile:
        text = ddscat_par.format(
                start_wave='0.{}'.format(wave_start),
                end_wave='0.{}'.format(wave_end),
                num_wave=wave_num,
		aeff=aeff,
            )
        parfile.write(text)

    with open('wave.pickle', 'wb') as wave:
        s = {
            'start_wavelength': wave_start,
            'end_wavelength': wave_end,
        }
        pickle.dump(s, wave)

    os.chdir('..')


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('subdir')
    argparser.add_argument('num_procs', type=int, default=30)
    argparser.add_argument('aeff', type=float, default=0.0126)
    args = argparser.parse_args()

    subprocess.call('rm -rf {}*'.format(args.subdir), shell=True)
    subprocess.call('mkdir {}/'.format(args.subdir), shell=True)
    subprocess.call('cp exec/* {}/'.format(args.subdir), shell=True)
    subprocess.call('cp shapes/shape_{dirs}.dat {dirs}/shape.dat'.format(dirs=args.subdir), shell=True)
    num_procs = args.num_procs

    start = 350 # in nm
    end = 800
    num = 451

    wavelengths_per = int(num / num_procs)
    excess = num % num_procs

    current = start
    wave_ranges = []

    for i in range(0, num_procs):
        first = current
        current += (wavelengths_per - 1)

        if excess:
            current += 1
            excess = excess - 1

        second = current
        wave_ranges.append((i, first, second))
        current += 1

    os.chdir(args.subdir)
    _ = [ddscat_split(wave_range, args.aeff) for wave_range in wave_ranges]
    os.chdir('..')

    # write pbs scripts
    list_script = '{}.pbs'.format(args.subdir)
    with open(list_script, 'w') as pbs:
        pbs.write(ddscat_pbs.format(
            max_sub=num_procs - 1,
            subdir=args.subdir,
        ))

    with open('reduce.pbs', 'w') as pbs:
        pbs.write(reduce_pbs.format(
            num_procs=num_procs,
            subdir=args.subdir,
        ))

    jobid = subprocess.check_output('qsub {}.pbs'.format(args.subdir), shell=True)
    jobid = str(jobid.decode('UTF-8')[:-1])
    subprocess.call(
        'qsub -W depend=afterokarray:{} reduce.pbs'.format(jobid), shell=True)


if __name__ == '__main__':
    main()

