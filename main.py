import fileorganizer.compare as foc


mode = 'compare'

if mode == 'compare':

    duplicate_dir = '/Users/sammcdonald/Pictures/Exported Photo Library/2020/03 March more'
    dir_untouched_original = '/Users/sammcdonald/Pictures/Exported Photo Library/2020/03 March'

    move_files = True
    foc.compare(duplicate_dir, dir_untouched_original, move_files)

elif mode == 'multcompare':

    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2018'
    dir_untouched_original = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/Screenshots'

    move_files = True
    foc.multcompare(duplicate_dir, dir_untouched_original, move_files)

elif mode == 'rename':
    print('\nRunning Rename operation\n')
