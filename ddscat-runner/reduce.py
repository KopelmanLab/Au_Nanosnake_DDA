import os
import os.path
import sys
import pickle
import glob
import argparse
import subprocess


def copy_file(filename, num_procs):
    with open(filename, 'w') as table:
        for i in range(0, num_procs):
            with open('{}_{}'.format(filename, i)) as subtable:
                for _ in range(14):
                    if i == 0:
                        table.write(subtable.read())
                    else:
                        _ = subtable.read()
                for line in subtable:
                    table.write(line)

    table_agg = []

    for i in range(0, num_procs):
        with open('{}_{}'.format(filename, i)) as subtable:
            for _ in range(14):
                if i == 0:
                    table_agg += subtable.readlines()
                else:
                    table_agg += subtable.readlines()[14:]

    with open(filename, 'w') as fp:
        _ = [fp.write(line) for line in table_agg]

def main():
    num_procs = int(sys.argv[1])
    wave_dirs = glob.glob('wavelengths_*')

    logs = []
    for directory in wave_dirs:
        pick_path = os.path.join(directory, 'log.pickle')

        with open(pick_path, 'rb') as pickle_log:
            logs.append(pickle.load(pickle_log))

    with open('final_output.pickle', 'wb') as final:
        pickle.dump(logs, final)


    files_to_copy = ['qtable', 'qtable2', 'mtable']
    _ = [copy_file(file, num_procs) for file in files_to_copy]
    files_to_remove = glob.glob('qtable_*') + glob.glob('mtable_*') + glob.glob('qtable2_*')

    for file in files_to_remove:
        subprocess.call('rm {}'.format(file), shell=True)

main()
