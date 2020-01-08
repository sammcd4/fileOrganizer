import fileorganizer as fo
import fileorganizer.comparator as foc
import os
from pathlib import Path

mode = 'multcompare'

if mode == 'compare':
    print('\nRunning comparision operation\n')

    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2018'
    dir_untouched_original = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/Screenshots'

    move_files = False
    comp = foc.Comparator(move_files)
    comp.compare_folders(duplicate_dir, dir_untouched_original)

elif mode == 'multcompare':
    print('\nRunning multiple comparision operation\n')

    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2018'
    dir_untouched_original = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/Screenshots'

    for f in os.listdir(duplicate_dir):
        pathdir = Path(duplicate_dir, f)
        if os.path.isdir(pathdir):
            move_files = False
            comp = foc.Comparator(move_files)
            comp.compare_folders(pathdir, dir_untouched_original)

elif mode == 'rename':
    print('\nRunning Rename operation\n')
