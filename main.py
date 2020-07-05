import fileorganizer.compare as foc

mode = 'compare'

# TODO: create one to many comparison scheme instead of just one to one or many in different folders

if mode == 'compare':

    # define directories to compare
    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2020/06 June old'
    dir_untouched_original = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2020/06 June'

    # compare
    foc.compare(duplicate_dir, dir_untouched_original)

# TODO: write unit tests for multcompare
# both flat and deep folder structure
# TODO: in multcompare mode, literally want to call compare multiple times so that comparision folder is in the correct spot?
elif mode == 'multcompare':

    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/_gsdata_/_saved_/Sam folder - to go through/extra music'
    dir_untouched_original = '/Volumes/Seagate 4/Seagate 2 Backup/Misc - Sam/extra music 1'

    foc.multcompare(duplicate_dir, dir_untouched_original)

elif mode == 'rename':
    print('\nRunning Rename operation\n')

elif mode == 'compare_exported':

    # parameters
    volume_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2020/'
    month_dir = '06 June'
    old_marker = ' old'

    # directories to compare
    duplicate_dir = volume_dir + month_dir + old_marker
    dir_untouched_original = volume_dir + month_dir

    # compare
    foc.compare(duplicate_dir, dir_untouched_original)