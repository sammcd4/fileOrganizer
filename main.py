import fileorganizer.compare as foc
import fileorganizer.utils as utils
import os
from pathlib import Path
import datetime
import time

mode = 'compare'

# TODO: create one to many comparison scheme instead of just one to one or many in different folders

if mode == 'exported':
    # specify which directory to check for duplicates
    year = '2022'
    month = '08 August'
    exported_path = '/Volumes/Seagate 5/Seagate 2 Backup/Photos + Videos/Exported Photo Library'

    # define directories to compare
    duplicate_dir = f'{exported_path}/{year}/{month} old'
    dir_untouched_original = f'{exported_path}/{year}/{month}'

    # compare
    foc.compare(duplicate_dir, dir_untouched_original) # exported should all be the similar extensions anyway.

elif mode == 'compare':

    # define directories to compare
    duplicate_dir = '/Users/sammcdonald/Desktop/Seagate 5/Seagate 2 Backup/1_Sam/Piano Sheet Music'
    dir_untouched_original = '/Volumes/Seagate 5/Seagate 2 Backup/1_Sam/Piano Sheet Music'

    # compare
    foc.compare(duplicate_dir, dir_untouched_original, ignore_extensions=True)

elif mode == 'update_dates':
    directory = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/2016 to sort'

    # For all WP_ files in the directory, update only the date to reflect the date in the filename
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # must be a WP_ file with date encoded into the filename
        if not filename.startswith('WP_'):
            continue

        date_str = filename.split('_')[1]

        # ensure that the datestr is all numeric
        if not date_str.isdigit():
            continue

        current_datetime = utils.get_creation_date(filepath)
        mod_time = time.mktime(current_datetime.timetuple())
        # TODO: This isn't working yet. Need to debug all of this

        # attach file time to datestr
        mod_time_str = str(mod_time).replace('.0', '')
        updated_mod_time_str = date_str + mod_time_str[-4:]

        # ensure that the mod time has the right number of characters
        if not len(updated_mod_time_str) == 12:
            print('Invalid mod time: {}'.format(updated_mod_time_str))
            continue

        updated_mod_time = int(updated_mod_time_str)

        print('Updating timestamp of file: {} to {}'.format(filepath, updated_mod_time))
        #os.utime(filepath, (updated_mod_time, updated_mod_time))


elif mode == 'remove_empty_folders':
    directory = '/Volumes/Seagate 4/Seagate 1 Backup/MusicS'
    utils.remove_empty_folders(directory, True)

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
            if False:
                foc.multcompare(duplicate_dir, orig_dir, ignore_extensions=True)
            else:
                # iterate only over the relevant month directories
                for f in os.listdir(duplicate_dir):
                    path_dir = Path(duplicate_dir, f)
                    if os.path.isdir(path_dir) and orig_dir.split('/')[-1] in str(path_dir):
                        foc.compare(path_dir, orig_dir, True, ignore_extensions=True)
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