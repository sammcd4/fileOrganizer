import fileorganizer as fo
import fileorganizer.comparator as foc

mode = 'compare'

if mode == 'compare':
    print('\nRunning comparision operation\n')

    duplicate_dir = '/Users/mcdonaldfamily/Documents/music to delete copy'
    dir_untouched_original = '/Users/mcdonaldfamily/Documents/music to delete'

    move_files = True
    comp = foc.Comparator(move_files)
    comp.compare_folders(duplicate_dir, dir_untouched_original)

elif mode == 'rename':
    print('\nRunning Rename operation\n')
