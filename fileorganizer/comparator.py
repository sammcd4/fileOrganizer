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

        # TODO Compare files of multiple similar file extensions
        # Possibly copy to a temp directory as a new name and then compare with that file instead?
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp


class Comparator:

    def __init__(self, move_duplicates=True):
        self.move_duplicates = move_duplicates
        self.duplicates_found = False
        self.left_only_found = []
        self.right_only_found = []

    def parse_comparison(self, dcmp):
        # alert of diff files found in these directories
        for name in dcmp.diff_files:
            print("diff_file found: {}\n\tdir1 {}\n\tdir2 {}".format(name, dcmp.left, dcmp.right))

        for name in dcmp.left_only:
            #print("\t{}".format(name))
            self.left_only_found.append(Path(dcmp.left, name))

        for name in dcmp.right_only:
            #print("\t{}".format(name))
            self.right_only_found.append(Path(dcmp.right, name))

        for sub_dcmp in dcmp.subdirs.values():
            self.parse_comparison(sub_dcmp)

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
        self.parse_comparison(dcmp)

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
            os.makedirs(Path(src_dir_parent, 'comparisons'))

        CompareInfo = namedtuple('CompareInfo', 'dir1, dir2, timestamp, move_dir')
        compareInfo = CompareInfo(dir1, dir2, timestamp_str, comparison_dir)

        if dcmp.same_files:
            self.duplicates_found = True
        else:
            print('\nNo duplicates found when comparing:\n\tdir1 {}\n\tdir2 {}\n'.format(dcmp.left, dcmp.right))

        self.move_duplicate_files(dcmp, compareInfo)

        if self.left_only_found:
            print("Unique files in dir 1: {}\n".format(dir1))
            for filepath in self.left_only_found:
                print("\t{}".format(filepath))

        # Do we need to display all of these files? TODO: Make a flag for this
        if False and self.right_only_found:
            print("Unique files in dir 2: {}\n".format(dir1))
            for filepath in self.right_only_found:
                print("\t{}".format(filepath))

    def move_duplicate_files(self, dcmp, compare_info):

        # TODO name could be different and still be a duplicate - how to manage this?
        for name in dcmp.same_files:
            print("same_file found: {}\n\tsrc {}\n\tdup {}".format(name, Path(dcmp.left, name), Path(dcmp.right, name)))

            if self.move_duplicates:
                right_relative = Path(dcmp.right).relative_to(compare_info.dir2)
                md = Path(compare_info.move_dir, str(right_relative))
                if not os.path.isdir(md):
                    os.makedirs(md)
                shutil.move(Path(dcmp.left, name), Path(md, name))
                print("\tmvd {}".format(Path(md, name)))

                # TODO apparently not all subdirectories are being removed
                # remove the directory if all files have been moved
                if not os.listdir(dcmp.left):
                    os.rmdir(dcmp.left)

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

