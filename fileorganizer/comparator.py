import os
import shutil
import filecmp
from datetime import datetime
from pathlib import Path
from collections import namedtuple
import fileorganizer.utils as utils


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
        # TODO Compare files of different file paths but same file
        # Possibly copy to a temp directory as a new name and then compare with that file instead?
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp


class Comparator:

    def __init__(self, move_duplicates=True, print_output=True):
        self.move_duplicates = move_duplicates
        self.duplicates_found = False
        self.left_only_found = []
        self.right_only_found = []
        self.dcmp = []
        self.print_output = print_output
        self.ignore_extensions = False

    def parse_comparison(self):
        # alert of diff files found in these directories
        for name in self.dcmp.diff_files:
            self.print("diff_file found: {}\n\tdir1 {}\n\tdir2 {}".format(name, self.dcmp.left, self.dcmp.right))

        for name in self.dcmp.left_only:
            #self.print("\t{}".format(name))
            self.left_only_found.append(Path(self.dcmp.left, name))

        for name in self.dcmp.right_only:
            #self.print("\t{}".format(name))
            self.right_only_found.append(Path(self.dcmp.right, name))

        # TODO: figure out what I was doing here recursively
        #for sub_dcmp in self.dcmp.subdirs.values():
        #    self.parse_comparison(sub_dcmp)

    def print(self, *args):
        if self.print_output:
            print(*args)

    # dir1 contains files to be moved to comparisons folder
    def compare_folders(self, dir1, dir2):
        # TODO: Use *args here?

        if self.ignore_extensions:
            # compare files with unchanged extensions for a baseline
            self.compare_folders_impl(dir1, dir2)

            # Find all extensions in dir1 and dir2
            ext_in_dir1 = utils.get_extensions(dir1)
            ext_in_dir2 = utils.get_extensions(dir2)

            for ext_dir2 in ext_in_dir2:

                # iterate over all convertible and see if ext_in_dir1 has one
                for convertible_ext in utils.get_convertible_extensions(ext_dir2):

                    if convertible_ext in ext_in_dir1:
                        # files of this extension need to be converted and placed in temp directory to compare with dir2

                        # Identify all files with this extension in dir1


                # Check for any files in dir1 that can be converted to dir2 extensions
                # For each of the convertible extensions from dir1 to dir2
                    # Track the dir1 files that I'm about to compare with
                    # Copy those files to a temporary directory
                    # Compare dir1_JPG_to_jpeg with dir2 and save same files
                    #
        else:
            return self.compare_folders_impl(dir1, dir2)

    def compare_folders_impl(self, dir1, dir2):

        if dir1 == '':
            if dir2 == '':
                self.print('dir1 and dir2 are empty')
            else:
                self.print('dir1 is empty')
            return None

        if dir2 == '':
            self.print('dir2 is empty')
            return None

        if False:
            # Determine the items that exist in both directories
            d1_contents = set(os.listdir(dir1))
            d2_contents = set(os.listdir(dir2))
            common = list(d1_contents & d2_contents)
            common_files = [f
                            for f in common
                            if os.path.isfile(os.path.join(dir1, f))
                            ]
            self.print('Common files:{}'.format(common_files))

            # Compare the directories
            match, mismatch, errors = filecmp.cmpfiles(dir1, dir2, common_files, shallow=False)

            self.print('Match:{}'.format(match))
            self.print('Mismatch:{}'.format(mismatch))
            self.print('Errors:{}'.format(errors))

        if not os.path.isdir(dir1):
            self.print('Non-existent directory: ', dir1)
            return False

        if not os.path.isdir(dir2):
            self.print('Non-existent directory: ', dir2)
            return False

        self.dcmp = Dircmp(dir1, dir2)
        if not self.dcmp: return False
        self.parse_comparison()

        # get current time for duplicates folder name
        obj = datetime.now()
        timestamp_str = obj.strftime("%d-%b-%Y-%H-%M-%S")
        self.print('Current Timestamp : ', timestamp_str)
        duplicate_folder = 'duplicates_' + timestamp_str

        # construct the comparisons folder to dump duplicate files
        src_dir = Path(dir1)
        src_dir_parent = src_dir.parent
        comparison_dir = Path(src_dir_parent, 'comparisons', duplicate_folder)
        if not os.path.isdir(Path(src_dir_parent, 'comparisons')):
            os.makedirs(Path(src_dir_parent, 'comparisons'))

        CompareInfo = namedtuple('CompareInfo', 'dir1, dir2, timestamp, move_dir')
        compareInfo = CompareInfo(dir1, dir2, timestamp_str, comparison_dir)

        if self.dcmp.same_files:
            self.duplicates_found = True
        else:
            self.print('\nNo duplicates found when comparing:\n\tdir1 {}\n\tdir2 {}\n'.format(self.dcmp.left, self.dcmp.right))

        self.move_duplicate_files(self.dcmp, compareInfo)

        if self.left_only_found:
            self.print("Unique files in dir 1: {}\n".format(dir1))
            #for filepath in self.left_only_found:
                #print("\t{}".format(filepath))

        # Do we need to display all of these files? TODO: Make a flag for this
        if False and self.right_only_found:
            self.print("Unique files in dir 2: {}\n".format(dir1))
            for filepath in self.right_only_found:
                self.print("\t{}".format(filepath))

        return True

    def move_duplicate_files(self, dcmp, compare_info):

        # TODO name could be different and still be a duplicate - how to manage this?
        for name in dcmp.same_files:
            self.print("same_file found: {}\n\tsrc {}\n\tdup {}".format(name, Path(dcmp.left, name), Path(dcmp.right, name)))

            if self.move_duplicates:
                right_relative = Path(dcmp.right).relative_to(compare_info.dir2)
                move_dir = Path(compare_info.move_dir, str(right_relative))
                if not os.path.isdir(move_dir):
                    os.makedirs(move_dir)
                shutil.move(Path(dcmp.left, name), Path(move_dir, name))
                self.print("\tmvd {}".format(Path(move_dir, name)))

                # TODO apparently not all subdirectories are being removed
                # remove the directory if all files have been moved
                if not os.listdir(dcmp.left):
                    os.rmdir(dcmp.left)

        for sub_dcmp in dcmp.subdirs.values():
            self.move_duplicate_files(sub_dcmp, compare_info)

    def move_duplicate_files2(self, compare_info):

        for name in compare_info.match:
            self.print("same_file {} found in {} and {}".format(name, compare_info.dir1, compare_info.dir2))
            md = compare_info.move_dir
            if not os.path.isdir(md):
                os.mkdir(md)
            shutil.move(Path(compare_info.dir1, name), Path(md, name))

        #for sub_dcmp in dcmp.subdirs.values():
        #    self.move_duplicate_files(sub_dcmp, compare_info)


def compare_legacy_to_latest(latest_dir, month_str):

    # for each latest directory, run automated comparison
    for m in month_str:
        self.print('\nRunning comparision operation\n')

        duplicate_dir = str(Path(latest_dir, m + ' latest'))
        dir_untouched_original = duplicate_dir.replace(' latest', '')

        # First compare as-is to capture all Live Photo movie file comparisons
        move_files = True
        comp = Comparator(move_files)
        comp.compare_folders(duplicate_dir, dir_untouched_original)

        # modify extensions to legacy Photo export and compare again
        utils.oldPhotosExtensions(duplicate_dir)
        comp.compare_folders(duplicate_dir, dir_untouched_original)
