import glob
import os
import os.path
import shutil
import sys


def pad_number(num):
    length = len(str(num))
    return ((3 - length) * '0') + str(num)

SUFFIXES = ['k000.E1', 'k000.E2', '.avg']

def main():
    assert(len(sys.argv) == 2)

    filepath = sys.argv[1]
    os.chdir(filepath)

    i = 0
    wavenumber = 0

    while True:
        subdir = 'wavelengths_{}'.format(i)
        i += 1

        checkdir = os.path.join(os.getcwd(), subdir)
        if not os.path.exists(checkdir):
            print(checkdir, ' does not exist')
            break

        j = 0

        while True:
            old_wavenum_str = 'w{}r000'.format(pad_number(j))
            new_waveum_str = 'w{}r000'.format(pad_number(wavenumber))

            j += 1
            wavenumber += 1

            if not os.path.exists(
                os.path.join(checkdir, old_wavenum_str + SUFFIXES[0])
            ):
                break

            for suffix in SUFFIXES:
                try:
                    src = os.path.join(checkdir, old_wavenum_str + suffix)
                    dst = os.path.join(os.getcwd(), new_waveum_str + suffix)

                    print("moving {} to {}".format(src, dst))

                    shutil.move(
                        src,
                        dst,
                    )

                except FileNotFoundError as e:
                    print(e)


if __name__ == "__main__":
    main()
