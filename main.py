import fileorganizer.compare as foc
import fileorganizer.utils as utils

mode = 'multcompare'

# TODO: create one to many comparison scheme instead of just one to one or many in different folders

if mode == 'compare':

    # define directories to compare
    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Video/Camera roll saved'
    dir_untouched_original = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2020/01 January'

    # compare
    foc.compare(duplicate_dir, dir_untouched_original)

elif mode == 'compare_exts':
    pass

elif mode == 'compare_mult_months':

    # define duplicate directory
    duplicate_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/recent photos backup/2016-2017_iMAC Exported Photos'

    # define set of original directory to compare against
    base_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2016/'
    orig_dirs = [(base_dir+month_dir_name) for month_dir_name in utils.get_month_folder_names()]

    # compare
    for orig_dir in orig_dirs:
        foc.compare(duplicate_dir, orig_dir)

# TODO: write unit tests for multcompare
# both flat and deep folder structure
# TODO: in multcompare mode, literally want to call compare multiple times so that comparision folder is in the correct spot?
elif mode == 'multcompare':

    duplicate_dir = '/Volumes/Seagate 5/Seagate 2 Backup/_gsdata_/_saved_/Photos + Videos/Exported Photo Library/2017'
    dir_untouched_orig_base = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2017/'
    dir_untouched_original = dir_untouched_orig_base + '03 March'

    # TODO: Got to add tests for multcompare if I'm using it so heavily here!
    if True:
        # optionally iterate of several orig dirs too
        orig_dirs = [(dir_untouched_orig_base + month_dir_name) for month_dir_name in utils.get_month_folder_names()]
        for orig_dir in orig_dirs:
            foc.multcompare(duplicate_dir, orig_dir, ignore_extensions=True)
    else:
        # only one original directory
        foc.multcompare(duplicate_dir, dir_untouched_original)

elif mode == 'rename':
    print('\nRunning Rename operation\n')

elif mode == 'compare_exported':

    # parameters
    volume_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2020/'
    month_dir = '08 August'
    old_marker = ' old 4'

    # directories to compare
    duplicate_dir = volume_dir + month_dir + old_marker
    dir_untouched_original = volume_dir + month_dir

    # compare
    foc.compare(duplicate_dir, dir_untouched_original)

# TODO: improve src/dup print outs when same_file found