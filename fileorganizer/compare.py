import fileorganizer.comparator as foc
from pathlib import Path
import os


def compare(duplicate_dir, dir_untouched_original, move_files=True, ignore_extensions=False):
    print('\nRunning comparision operation\n')

    comp = foc.Comparator(move_files, ignore_extensions=ignore_extensions)
    comp.compare_folders(duplicate_dir, dir_untouched_original)


def multcompare(duplicate_dir, dir_untouched_original, move_files=True, ignore_extensions=False):
    print('\nRunning multiple comparision operation\n')

    for f in os.listdir(duplicate_dir):
        path_dir = Path(duplicate_dir, f)
        if os.path.isdir(path_dir):
            compare(path_dir, dir_untouched_original, move_files, ignore_extensions=ignore_extensions)


if __name__ == '__main__':

    duplicate_dir = ''
    dir_untouched_original = ''

    compare(duplicate_dir, dir_untouched_original)