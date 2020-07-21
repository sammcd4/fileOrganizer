import os
import glob
from pathlib import Path

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


def get_file_size(file, unit=None):
    return round(convert_bytes(os.path.getsize(file), unit), 3)


def convert_bytes(size, unit=None):
    factor = 1000 # non-binary conversion
    if unit == "KB":
        return size / factor
    elif unit == "MB":
        return size / (factor * factor)
    elif unit == "GB":
        return size / (factor * factor * factor)
    else:
        return size


def get_num_files(directory, ext):
    # use glob.glob to search for files with the specified extension
    return len(glob.glob(directory + '/**/*' + ext, recursive=True))


def get_types_from_folder(directory):

    types_dict = {}

    # extensions
    photo_exts = ['.jpg', '.JPG', '.JPEG', '.jpeg']
    video_exts = ['.mov', '.MOV', '.AVI', '.avi', '.mpg', '.MPG', '.m4v', '.M4V']
    live_photo_ext = ['LivePhoto.jpg', 'LivePhoto.JPG']
    live_photo_mov_ext = ['LivePhoto.mov', 'LivePhoto.MOV']
    screenshot_exts = ['.png', '.PNG']
    raw_exts = ['.cr2', '.CR2']

    # find all photos
    num_photos_glob = 0
    for photo_ext in photo_exts:
        num_photos_glob += get_num_files(directory, photo_ext)

    file_count = get_num_files(directory, '.*')

    # initialize count and size
    num_photos = 0
    size_photos = 0

    num_live_photos = 0
    size_live_photos = 0

    num_live_photos_mov = 0
    size_live_photos_mov = 0

    num_videos = 0
    size_videos = 0

    num_screenshots = 0
    size_screenshots = 0

    num_raw_photos = 0
    size_raw_photos = 0

    # find all file types (count and size)
    files = Path(directory).rglob('**/*.*')
    for file in files:

        # because path is object not string
        file_str = str(file)

        # ignore DS_Store files on mac
        if '.DS_Store' in file_str:
            continue

        # get type, count, size
        print(file_str)

        if any(ext in file_str for ext in live_photo_ext):
            # Live Photo
            num_live_photos += 1
            size_live_photos += get_file_size(file, 'MB')

        elif any(ext in file_str for ext in live_photo_mov_ext):
            # Live Photo videos
            num_live_photos_mov += 1
            size_live_photos_mov += get_file_size(file, 'MB')

        elif any(ext in file_str for ext in photo_exts):
            # Photo
            num_photos += 1  # increment
            size_photos += get_file_size(file, 'MB')

        elif any(ext in file_str for ext in video_exts):
            # Video
            num_videos += 1  # increment
            size_videos += get_file_size(file, 'MB')

        elif any(ext in file_str for ext in screenshot_exts):
            # Screenshots
            num_screenshots += 1  # increment
            size_screenshots += get_file_size(file, 'MB')

        elif any(ext in file_str for ext in raw_exts):
            # Raw photos
            num_raw_photos += 1  # increment
            size_raw_photos += get_file_size(file, 'MB')


    # calculate photo count and size (accounting for LivePhotos)
    types_dict['photo'] = {}
    #print('num_photos = {}'.format(num_photos))
    #print('num_live_photos = {}'.format(num_live_photos))
    #print('num_photos_glob = {}'.format(num_photos_glob))
    assert num_photos + num_live_photos == num_photos_glob
    types_dict['photo']['count'] = num_photos
    types_dict['photo']['size'] = size_photos

    # live photos
    types_dict['livephoto'] = {}
    types_dict['livephoto']['count'] = num_live_photos
    types_dict['livephoto']['size'] = size_live_photos

    # live photo videos
    types_dict['livephotovideo'] = {}
    types_dict['livephotovideo']['count'] = num_live_photos_mov
    types_dict['livephotovideo']['size'] = size_live_photos_mov

    # videos
    types_dict['video'] = {}
    types_dict['video']['count'] = num_videos
    types_dict['video']['size'] = size_videos

    # screenshots
    types_dict['screenshot'] = {}
    types_dict['screenshot']['count'] = num_screenshots
    types_dict['screenshot']['size'] = size_screenshots

    # raw photos
    types_dict['raw'] = {}
    types_dict['raw']['count'] = num_raw_photos
    types_dict['raw']['size'] = size_raw_photos

    # verify that all files have been counted and sized
    file_counter = 0
    for type, data in types_dict.items():
        file_counter += data['count']
    assert file_count == file_counter
    print('All files have been counted and sized')

    return types_dict


if __name__ == '__main__':
    directory1 = '/Users/sammcdonald/Documents/photos'
    print(get_types_from_folder(directory1))
