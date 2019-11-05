import os
import shutil
import filecmp
from datetime import datetime
from pathlib import Path
from collections import namedtuple


class Dircmp(filecmp.dircmp):
    """
    Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
    subclass compares the content of files with the same path.
    """
    def phase3(self):
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp


class Comparator:
    move_duplicates = True

    def __init__(self):
        self.move_duplicates = False

    def print_diff_files(self, dcmp):
        for name in dcmp.diff_files:
            print("diff_file {} found in {} and {}".format(name, dcmp.left, dcmp.right))

        for sub_dcmp in dcmp.subdirs.values():
            self.print_diff_files(sub_dcmp)

    def compare_folders(self, dir1, dir2):

        if dir1 == '':
            if dir2 == '':
                print('dir1 and dir2 are empty')
            else:
                print('dir1 is empty')
            return

        if dir2 == '':
            print('dir2 is empty')
            return

        if False:
            # Determine the items that exist in both directories
            d1_contents = set(os.listdir(dir1))
            d2_contents = set(os.listdir(dir2))
            common = list(d1_contents & d2_contents)
            common_files = [f
                            for f in common
                            if os.path.isfile(os.path.join(dir1, f))
                            ]
            print('Common files:{}'.format(common_files))

            # Compare the directories
            match, mismatch, errors = filecmp.cmpfiles(dir1, dir2, common_files, shallow=False)

            print('Match:{}'.format(match))
            print('Mismatch:{}'.format(mismatch))
            print('Errors:{}'.format(errors))
        
        dcmp = Dircmp(dir1, dir2)
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

        if self.move_duplicates:
            self.move_duplicate_files2(compareInfo)

    def move_duplicate_files(self, dcmp, compare_info):

        for name in dcmp.same_files:
            print("same_file {} found in {} and {}".format(name, dcmp.left, dcmp.right))
            md = compare_info.move_dir
            if not os.path.isdir(md):
                os.mkdir(md)
            shutil.move(Path(dcmp.left, name), Path(md, name))

        for sub_dcmp in dcmp.subdirs.values():
            self.move_duplicate_files(sub_dcmp, compare_info)

    def move_duplicate_files2(self, compare_info):

        for name in compare_info.match:
            print("same_file {} found in {} and {}".format(name, compare_info.dir1, compare_info.dir2))
            md = compare_info.move_dir
            if not os.path.isdir(md):
                os.mkdir(md)
            shutil.move(Path(compare_info.dir1, name), Path(md, name))

        #for sub_dcmp in dcmp.subdirs.values():
        #    self.move_duplicate_files(sub_dcmp, compare_info)

