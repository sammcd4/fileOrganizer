import os
import shutil
import filecmp
from datetime import datetime
from pathlib import Path
from collections import namedtuple


class Comparator:

    def __init__(self):
        print('Building Comparator')

    def print_diff_files(self, dcmp):
        for name in dcmp.diff_files:
            print("diff_file {} found in {} and {}".format(name, dcmp.left, dcmp.right))

        for sub_dcmp in dcmp.subdirs.values():
            self.print_diff_files(sub_dcmp)

    def compare_folders(self, dir1, dir2):

        dcmp = filecmp.dircmp(dir1, dir2)
        self.print_diff_files(dcmp)

        # get current time for duplicates folder name
        obj = datetime.now()
        timestamp_str = obj.strftime("%d-%b-%Y-%H-%M-%S")
        print('Current Timestamp : ', timestamp_str)
        duplicate_folder = 'duplicates_' + timestamp_str

        # construct the comparisons folder to dump duplicate files
        src_dir = Path(dir1)
        src_dir_parent = src_dir.parent
        comparison_dir = Path(src_dir_parent, 'comparisons', duplicate_folder)
        if not os.path.isdir(Path(src_dir_parent, 'comparisons')):
            os.mkdir(Path(src_dir_parent, 'comparisons'))

        CompareInfo = namedtuple('CompareInfo', 'dir1, dir2, timestamp, move_dir')
        compareInfo = CompareInfo(dir1, dir2, timestamp_str, comparison_dir)

        self.move_duplicate_files(dcmp, compareInfo)

    def move_duplicate_files(self, dcmp, compare_info):

        for name in dcmp.same_files:
            print("same_file {} found in {} and {}".format(name, dcmp.left, dcmp.right))
            md = compare_info.move_dir
            if not os.path.isdir(md):
                os.mkdir(md)
            shutil.move(Path(dcmp.left, name), Path(md, name))

        for sub_dcmp in dcmp.subdirs.values():
            self.move_duplicate_files(sub_dcmp, compare_info)

