import os
import shutil
import filecmp
from datetime import datetime
from pathlib import Path
from collections import namedtuple


def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file {} found in {} and {}".format(name, dcmp.left, dcmp.right))

    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

def compare_folders(dir1, dir2):

    dcmp = filecmp.dircmp(dir1, dir2)
    print_diff_files(dcmp)

    # get current time for duplicates folder name
    obj = datetime.now()
    timestamp_str = obj.strftime("%d-%b-%Y-%H-%M-%S")
    print('Current Timestamp : ', timestamp_str)
    duplicate_folder = 'duplicates_' + timestamp_str

    # construct the comparisons folder to dump duplicate files
    src_dir = Path(dir1)
    src_dir_parent = src_dir.parent
    comparison_dir = Path(src_dir_parent, 'comparisons', duplicate_folder)

    CompareInfo = namedtuple('CompareInfo', 'dir1, dir2, timestamp, move_dir')
    compareInfo = CompareInfo(dir1, dir2, timestamp_str, comparison_dir)

    move_duplicate_files(dcmp, compareInfo)


def move_duplicate_files(dcmp, compareInfo):

    for name in dcmp.same_files:
        print("same_file {} found in {} and {}".format(name, dcmp.left, dcmp.right))
        if not os.path.isdir(compareInfo.move_dir):
            os.mkdir(compareInfo.move_dir)
        shutil.move(Path(dcmp.left, name), Path(compareInfo.move_dir, name))

    for sub_dcmp in dcmp.subdirs.values():
        move_duplicate_files(sub_dcmp, compareInfo)


mode = 'compare'
dir1 = '/Volumes/Seagate 2/Photos + Videos/Exported Photo Library/2019/09_30 September'
dir2 = '/Volumes/Seagate 2/Photos + Videos/Exported Photo Library/2019/09 September'
compare_folders(dir1, dir2)
