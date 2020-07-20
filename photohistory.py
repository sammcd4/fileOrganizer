import os
import glob

# Methods to extract count and size of photos/videos for each month

def get_ext_from_folder(directory):
    # returns a dictionary of key-value pairs of file extension and number of files
    ext_dict = {}

    # get all files from the folder

    return ext_dict


def parse_types(types_dict):
    # given a dictionary of types, return a new dictionary of generalized types, based on what is being logged
    # e.g. jpg, JPG, jpeg are all Photo, so combine all those under photo
    types_dict = {}

    return types_dict


def get_num_files(directory, ext):
    # use glob.glob to search for files with the specified extension
    return len(glob.glob(directory + '/**/*' + ext, recursive=True))


def get_types_from_folder(directory):

    types_dict = {}

    # find all Live Photos

    # find all photos
    photo_exts = ['.jpg', '.JPG', '.JPEG', '.jpeg']
    num_photos = 0
    for photo_ext in photo_exts:
        num_photos += get_num_files(directory, photo_ext)
    types_dict['photo'] = num_photos

    return types_dict


if __name__ == '__main__':
    directory1 = '/Volumes/Seagate 5/Seagate 2 Backup/Photos + Videos/2017/2017_07-09_rock park,hair cut '
    print(get_types_from_folder(directory1))