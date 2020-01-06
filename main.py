import fileorganizer as fo
import fileorganizer.comparator as foc

mode = 'compare'

if mode == 'compare':
    print('\nRunning comparision operation\n')

    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2019/12 December latest'
    dir_untouched_original = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2019/12 December'

    move_files = True
    comp = foc.Comparator(move_files)
    comp.compare_folders(duplicate_dir, dir_untouched_original)

elif mode == 'rename':
    print('\nRunning Rename operation\n')
