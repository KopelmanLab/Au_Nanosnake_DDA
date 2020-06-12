import os
import time
import subprocess
import argparse
import pickle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirno', type=int)
    args = parser.parse_args()

    os.chdir('wavelengths_{}'.format(args.dirno))

    time_taken = None

    start_time = time.time()

    with open('log.out', 'w') as log:
        subprocess.call('./ddscat', shell=True, stdout=log, stderr=log)

    end_time = time.time()

    time_taken = end_time - start_time

    with open('wave.pickle', 'rb') as wave:
        ex = pickle.load(wave)

    s = {
        'start_wavelength': ex['start_wavelength'],
        'end_wavelength': ex['end_wavelength'],
        'start_time': start_time,
        'end_time': end_time,
        'time_taken': time_taken,
    }

    with open('log.pickle', 'wb') as log:
        pickle.dump(s, log)

    subprocess.call('mv qtable ../qtable_{}'.format(args.dirno), shell=True)
    subprocess.call('mv qtable2 ../qtable2_{}'.format(args.dirno), shell=True)
    subprocess.call('mv mtable ../mtable_{}'.format(args.dirno), shell=True)


main()
