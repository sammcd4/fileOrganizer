import fileorganizer.compare as foc
import fileorganizer.utils as utils
import os
from pathlib import Path
import datetime
import time

mode = 'multcompare_both'

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
    duplicate_dir = '/Volumes/My Book 6/_saved_/Photos + Videos/100__TSB _to organize'
    dir_untouched_original = '/Volumes/Seagate 5/Seagate 2 Backup/Photos + Videos/2019'

    # compare
    foc.compare(duplicate_dir, dir_untouched_original, ignore_extensions=False)
elif mode == 'multcompare_orig_organized':
    # directory with raw files to compare (to delete)
    single_duplicate_dir = '/Volumes/My Book 6/_saved_/Photos + Videos/2012/2012_First Married Year Adventures/Sam\'s Birthday'

    # directory containing organized subdirectories containing files (originals)
    untouched_original_dir = '/Volumes/Seagate 5/Seagate 2 Backup/Photos + Videos/2012'

    # iterate over all subdirectories in original dir and search for files to delete from single duplicate dir
    # feature{print_compare_summary_for_multiple_subdir_comparisons} provide a summary when foc.compare called multiple times. Use output to summarize total, or absorb this functionality into foc class
    for subdir, dirs, files in os.walk(untouched_original_dir):
        for untouched_original_subdir in dirs:
            # print(f'comparing orig subdir: {os.path.join(subdir, untouched_original_subdir)} with duplicate_dir: {single_duplicate_dir}')
            foc.compare(single_duplicate_dir, os.path.join(subdir, untouched_original_subdir), ignore_extensions=False)

elif mode == 'multcompare_both':
    # directory with subdirectories to compare (to delete)
    duplicate_dir = '/Volumes/My Book 6/_saved_/Photos + Videos/2015'

    # directory containing organized subdirectories containing files (originals)
    untouched_original_dir = '/Volumes/Seagate 5/Seagate 2 Backup/Photos + Videos/2015'

    for d_subdir, d_dirs, _ in os.walk(duplicate_dir):
        for duplicate_subdir in d_dirs:

            # iterate over all subdirectories in original dir and search for files to delete from single duplicate dir
            # feature{print_compare_summary_for_multiple_subdir_comparisons} provide a summary when foc.compare called multiple times. Use output to summarize total, or absorb this functionality into foc class
            for subdir, dirs, files in os.walk(untouched_original_dir):
                for untouched_original_subdir in dirs:
                    # print(f'comparing orig subdir: {os.path.join(subdir, untouched_original_subdir)} with duplicate_dir: {os.path.join(d_subdir, duplicate_subdir)}')
                    foc.compare(os.path.join(d_subdir, duplicate_subdir), os.path.join(subdir, untouched_original_subdir), ignore_extensions=False)

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

    duplicate_dir = '/Volumes/My Book 6/_saved_/Photos + Videos/Exported Photo Library/2016'
    dir_untouched_orig_base = '/Volumes/My Book 6/Backup/Photos + Videos/Exported Photo Library/2016/'
    

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
                        # TODO fix which paths are compared here
                        # print(orig_dir.split('/')[-1])
                        # print(f'dup: {path_dir}\ncompared with\norig_dir: {orig_dir}')
    else:
        dir_untouched_original = dir_untouched_orig_base + '03 March'
        # only one original directory
        foc.multcompare(duplicate_dir, dir_untouched_original)

elif mode == 'rename':
    print('\nRunning Rename operation\n')

elif mode == 'compare_exported':

    # parameters
    drive = '/Volumes/My Book 6/Backup/'
    volume_dir = 'Photos + Videos/Exported Photo Library/2016/'
    month_dir = '03 March'
    old_marker = ''

    dup_base_dir = '/Volumes/My Book 6/_saved_/Photos + Videos/Exported Photo Library/2016/'

    # directories to compare
    # duplicate_dir = drive + volume_dir + month_dir + old_marker
    duplicate_dir = dup_base_dir + month_dir + old_marker
    # duplicate_dir = '/Volumes/My Book 6/_saved_/Photos + Videos/Exported Photo Library/2020 imported 2/06 June imported'
    dir_untouched_original = drive + volume_dir + month_dir

    # compare
    foc.compare(duplicate_dir, dir_untouched_original, ignore_extensions=False)

elif mode == 'mult_compare_exported':

    duplicate_dir = '/Volumes/My Book 6/_saved_/Photos + Videos/Exported Photo Library/2020/'
    dir_untouched_orig_base = '/Volumes/My Book 6/Backup/Photos + Videos/Exported Photo Library/2020/'


# TODO: improve src/dup print outs when same_file found