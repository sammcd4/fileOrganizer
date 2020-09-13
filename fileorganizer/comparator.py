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

    def __init__(self, move_duplicates=True, print_output=True, ignore_extensions=False):
        self.move_duplicates = move_duplicates
        self.duplicates_found = False
        self.left_only_found = []
        self.right_only_found = []
        self.dcmp = []
        self.print_output = print_output
        self.ignore_extensions = ignore_extensions
        self.comparisons_dir = ''
        self.duplicates_dir = ''
        self.reuse_duplicates_dir = False
        self.cleanup_tmp_dir = True

    def parse_comparison(self, dcmp):

        # alert of diff files found in these directories
        for name in dcmp.diff_files:
            self.print("diff_file found: {}\n\tdir1 {}\n\tdir2 {}".format(name, self.dcmp.left, self.dcmp.right))

        # TODO: feature{compare_diff_ext} Only count left only if all comparisons have left only
        for name in dcmp.left_only:
            #self.print("\t{}".format(name))
            if self.ignore_extensions:
                pass
            else:
                self.left_only_found.append(Path(self.dcmp.left, name))

        #  TODO: feature{compare_diff_ext} Only count right only if all comparisons have right only
        for name in dcmp.right_only:
            #self.print("\t{}".format(name))
            if self.ignore_extensions:
                pass
            else:
                self.right_only_found.append(Path(self.dcmp.right, name))

        # TODO: figure out what I was doing here recursively
        for sub_dcmp in dcmp.subdirs.values():
            self.parse_comparison(sub_dcmp)

    def print(self, *args):
        if self.print_output:
            print(*args)

    # dir1 contains files to be moved to comparisons folder
    def compare_folders(self, dir1, dir2):
        # TODO: Use *args here?

        if self.ignore_extensions:
            # compare files with unchanged extensions for a baseline
            self.compare_folders_impl(dir1, dir2)
            self.reuse_duplicates_dir = True

            # Find all extensions in dir1 and dir2
            ext_in_dir1 = utils.get_extensions(dir1)
            ext_in_dir2 = utils.get_extensions(dir2)

            base_comparisons_dir = self.comparisons_dir

            for matching_ext in ext_in_dir2:

                # iterate over all convertible and see if ext_in_dir1 has one
                for convertible_ext in utils.get_convertible_extensions(matching_ext):

                    if convertible_ext in ext_in_dir1:
                        # files of this extension need to be converted and placed in temp directory to compare with dir2

                        # Identify all files with this extension in dir1
                        orig_files = utils.get_files_with_ext(dir1, convertible_ext)

                        # Copy all those convertible files to a temp directory
                        tmp_dir_name = 'dir1_' + convertible_ext.replace('.', '') + '_to_' + matching_ext.replace('.', '')
                        # self.duplicates_dir should be assigned because compare_folders(dir1, dir2) has been called
                        tmp_dir1 = Path(base_comparisons_dir, tmp_dir_name)
                        utils.mkdir(tmp_dir1)

                        # Convert all files that match this extension, preserving file path
                        # This copies the files into their respective tmp directories prior to comparison
                        self.print('Converting all files into temp directory with new extension...')
                        for orig_file in orig_files:
                            relative_file_path = Path(orig_file).relative_to(dir1)
                            orig_file_name = os.path.basename(orig_file)
                            relative_file_path_parent = str(relative_file_path).replace(orig_file_name, '')

                            # save the same file with a different extension that matches dir2
                            converted_file_name = orig_file_name.replace(convertible_ext, matching_ext)
                            if os.path.isfile(orig_file):
                                shutil.copy(orig_file, os.path.join(tmp_dir1, relative_file_path_parent, converted_file_name))
                        self.print('Finished converting all files')

                        # Now that all relevant files are in the tmp directory, make the comparison
                        self.compare_folders_impl(tmp_dir1, dir2)

                        # TODO: Copied code from compare_folders_impl because need separately here
                        if self.dcmp.same_files:
                            self.duplicates_found = True

                        # If same files were found here, then they need to be moved from dir1 with the original extension
                        self.move_duplicate_files(self.dcmp, dir1, file_extension=convertible_ext)

                        if self.left_only_found:
                            self.print("Unique files in dir 1: {}\n".format(dir1))
                            # for filepath in self.left_only_found:
                            # print("\t{}".format(filepath))

                        # Do we need to display all of these files? TODO: Make a flag for this
                        if False and self.right_only_found:
                            self.print("Unique files in dir 2: {}\n".format(dir2))
                            for filepath in self.right_only_found:
                                self.print("\t{}".format(filepath))

                        # Cleanup this temp directory for this convertible extension
                        if self.cleanup_tmp_dir:
                            shutil.rmtree(tmp_dir1, ignore_errors=True)

                        # Cleanup the extra comparisons directory generated by comparing tmp dirs
                        if self.cleanup_tmp_dir:
                            shutil.rmtree(self.comparisons_dir, ignore_errors=True)

            # Cleanup compare_diff_ext settings
            self.reuse_duplicates_dir = False

            return True
        else:
            return self.compare_folders_impl(dir1, dir2)

    def compare_folders_impl(self, dir1, dir2):

        # TODO: feature{better_dir1_dir2} Need to make clear which is which with better naming (e.i. dup_dir, orig_dir)
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
        if not self.dcmp:
            return False
        self.parse_comparison(self.dcmp)

        # Know where to create comparisons dir
        src_dir = Path(dir1)
        src_dir_parent = src_dir.parent

        # TODO: feature{compare_diff_ext} replace ignore_extension with something like compare_diff_ext or something
        # only assign new duplicates dir if not wanting to reuse (will reuse in ignore_extension workflow)
        if not self.reuse_duplicates_dir:
            # get current time for duplicates folder name
            obj = datetime.now()
            timestamp_str = obj.strftime("%d-%b-%Y-%H-%M-%S")
            self.print('Current Timestamp : ', timestamp_str)
            duplicate_folder = 'duplicates_' + timestamp_str
            # TODO: feature{compare_diff_ext} Need a way to reuse/assign the duplicate folder name when doing all new compare
            # operations with ignore_extension workflow. This will ensure that a single duplicates folder is created for the
            # compare operation instead of like 5 or 6.

            # construct the comparisons folder to dump duplicate files
            duplicates_dir = Path(src_dir_parent, 'comparisons', duplicate_folder)
            self.duplicates_dir = duplicates_dir

        self.comparisons_dir = Path(src_dir_parent, 'comparisons')
        if not os.path.isdir(Path(src_dir_parent, 'comparisons')):
            os.makedirs(Path(src_dir_parent, 'comparisons'))

        if self.dcmp.same_files:
            self.duplicates_found = True
        else:
            self.print('\nNo duplicates found when comparing:\n\tdir1 {}\n\tdir2 {}\n'.format(self.dcmp.left, self.dcmp.right))

        self.move_duplicate_files(self.dcmp, dir1)

        if self.left_only_found:
            self.print("Unique files in dir 1: {}\n".format(dir1))
            #for filepath in self.left_only_found:
                #print("\t{}".format(filepath))

        # Do we need to display all of these files? TODO: Make a flag for this
        if False and self.right_only_found:
            self.print("Unique files in dir 2: {}\n".format(dir2))
            for filepath in self.right_only_found:
                self.print("\t{}".format(filepath))

        return True

    def move_duplicate_files(self, dcmp, src_dir, file_extension=None):
        # This method takes the results of the dcmp and for all in dcmp.same_files, move those files
        # optional file_extension argument is used to ignore extension of file used in dcmp.same_files
        # and overwrite it with the provided file extension. This facilitates different extensions being
        # compared and moved

        # src_dir is used to configure the relative path to the file being moved, but ignore_extensions messes with the
        # assumption that dcmp.left is relative to src_dir. Logic is added to simply eliminate the relative path when
        # file_extension is not None
        if file_extension is None:
            left_dir = dcmp.left
        else:
            left_dir = src_dir

        # TODO: feature{compare_diff_name} name could be different and still be a duplicate - how to manage this?
        for name in dcmp.same_files:
            self.print("same_file found: {}\n\tsrc {}\n\tdup {}".format(name, Path(left_dir, name), Path(dcmp.right, name)))

            if self.move_duplicates:
                left_relative = Path(left_dir).relative_to(src_dir)
                move_dir = Path(self.duplicates_dir, str(left_relative))
                if not os.path.isdir(move_dir):
                    os.makedirs(move_dir)

                # Change extension or not
                if file_extension is None:
                    file_name = name
                else:
                    file, ext = os.path.splitext(name)
                    file_name = file + file_extension

                self.print("\tfile {} should have ext {}".format(file_name, file_extension))
                # Move the duplicate file
                shutil.move(Path(left_dir, file_name), Path(move_dir, file_name))
                self.print("\tmvd {}".format(Path(move_dir, file_name)))

                # TODO apparently not all subdirectories are being removed
                # remove the directory if all files have been moved
                if not os.listdir(left_dir):
                    os.rmdir(left_dir)

        for sub_dcmp in dcmp.subdirs.values():
            self.move_duplicate_files(sub_dcmp, src_dir, file_extension)


def compare_legacy_to_latest(latest_dir, month_str):

    # for each latest directory, run automated comparison
    for m in month_str:
        print('\nRunning comparision operation\n')

        duplicate_dir = str(Path(latest_dir, m + ' latest'))
        dir_untouched_original = duplicate_dir.replace(' latest', '')

        # First compare as-is to capture all Live Photo movie file comparisons
        move_files = True
        comp = Comparator(move_files)
        comp.compare_folders(duplicate_dir, dir_untouched_original)

        # modify extensions to legacy Photo export and compare again
        utils.oldPhotosExtensions(duplicate_dir)
        comp.compare_folders(duplicate_dir, dir_untouched_original)
