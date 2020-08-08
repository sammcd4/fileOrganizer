import os
import glob
from pathlib import Path
import xlwt
from xlwt import Workbook
from PIL import Image
from PIL.ExifTags import TAGS

# Methods to extract count and size of photos/videos for each month
# TODO: make photohistory class to encapsulate methods and printing options


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


def init_types(types):
    type_dict = {}
    for a_type in types:
        type_dict[a_type] = {}
        type_dict[a_type]['count'] = 0
        type_dict[a_type]['size'] = 0

    return type_dict


def update_type(types_dict, a_type, file):
    types_dict[a_type]['count'] += 1
    types_dict[a_type]['size'] += get_file_size(file, 'MB')


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
    types_list = ['applephoto', 'livephoto', 'livephotovideo',
                  'video', 'photo',
                  'screenshot', 'raw',
                  'other']
    types_dict = init_types(types_list)
    #print(types_dict)

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
            update_type(types_dict, 'livephoto', file)

        elif any(ext in file_str for ext in live_photo_mov_ext):
            # Live Photo videos
            update_type(types_dict, 'livephotovideo', file)

        elif any(ext in file_str for ext in photo_exts):
            # Photo

            # determine if the source was an Apple device
            is_apple_photo = False
            # read the image data using PIL
            image = Image.open(file)
            # extract EXIF data
            exifdata = image.getexif()
            # iterating over all EXIF data fields
            for tag_id in exifdata:
                # get the tag name, instead of human unreadable tag id
                tag = TAGS.get(tag_id, tag_id)

                if tag == 'Make':
                    data = exifdata.get(tag_id)
                    # decode bytes
                    if isinstance(data, bytes):
                        data = data.decode()
                    if data == 'Apple':
                        is_apple_photo = True
                        break

            if is_apple_photo:
                photo_type = 'applephoto'
                print('Found photo taken from Apple device')
            else:
                photo_type = 'photo'

            update_type(types_dict, photo_type, file)

        elif any(ext in file_str for ext in video_exts):
            # Video
            update_type(types_dict, 'video', file)

        elif any(ext in file_str for ext in screenshot_exts):
            # Screenshots
            update_type(types_dict, 'screenshot', file)

        elif any(ext in file_str for ext in raw_exts):
            # Raw photos
            update_type(types_dict, 'raw', file)

        else:
            # Other files
            update_type(types_dict, 'other', file)

    # verify count of all photos, otherwise exit
    assert types_dict['applephoto']['count'] + types_dict['photo']['count'] + types_dict['livephoto']['count'] == num_photos_glob

    # verify that all files have been counted and sized
    file_counter = 0
    for type, data in types_dict.items():
        file_counter += data['count']
    assert file_count == file_counter
    print('All files have been counted and sized')

    return types_dict


def write_excel(types_dict):

    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')

    iter = 0
    for a_type, value in types_dict.items():
        sheet1.write(0, iter, a_type + '_count')
        sheet1.write(1, iter, types_dict[a_type]['count'])
        iter += 1
        sheet1.write(0, iter, a_type + '_size')
        sheet1.write(1, iter, types_dict[a_type]['size'])
        iter += 1

    wb.save('types_data.xls')


if __name__ == '__main__':
    directory1 = '/Users/sammcdonald/Documents/photos'
    types_dict = get_types_from_folder(directory1)
    print(types_dict)

    # TODO: Read from excel file and choose to add to values that already exist there
    # TODO: Have one excel to read from and a different one to write to, to preserve data
    # TODO: Description column just with the directory
    # TODO: Way to automate all the folders, since this only works for one right now.
    # TODO: Come up with format of excel file for several folders, probably just rows for each unique subdirectory
    # TODO: Incorporate some logic based on the date. Need a way to only log ones for a particular month/year
    # TODO: Write tests for photohistory, including date range filtering
    # TODO: Have a sheet for each month/year or something?
    write_excel(types_dict)
