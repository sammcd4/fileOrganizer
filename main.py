import fileorganizer as fo
import fileorganizer.comparator as foc

mode = 'compare'

if mode == 'compare':
    print('\nRunning comparision operation\n')

    duplicate_dir = '/Users/mcdonaldfamily/Documents/Missy + Teresa Raw'
    dir_untouched_original = '/Volumes/Seagate 2/Photos + Videos/2019_05_Zac Teresa Syd'

    comp = foc.Comparator()
    comp.compare_folders(duplicate_dir, dir_untouched_original)

elif mode == 'rename':
    print('\nRunning Rename operation\n')
