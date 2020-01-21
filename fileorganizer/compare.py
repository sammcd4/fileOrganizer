import fileorganizer.comparator as foc
from pathlib import Path
import os


def compare(duplicate_dir, dir_untouched_original, move_files=True):
    print('\nRunning comparision operation\n')

    comp = foc.Comparator(move_files)
    comp.compare_folders(duplicate_dir, dir_untouched_original)


def multcompare(duplicate_dir, dir_untouched_original, move_files=True):
    print('\nRunning multiple comparision operation\n')

    for f in os.listdir(duplicate_dir):
        path_dir = Path(duplicate_dir, f)
        if os.path.isdir(path_dir):
            compare(duplicate_dir, dir_untouched_original, move_files)


if __name__ == '__main__':

    duplicate_dir = ''
    dir_untouched_original = ''

    compare(duplicate_dir, dir_untouched_original)