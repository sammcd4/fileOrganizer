import os
import glob
from pathlib import Path
import xlwt
from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy
from PIL import Image
from PIL.ExifTags import TAGS
import itertools
import fileorganizer.utils as utils
from datetime import date, datetime
from calendar import monthrange
import platform

# Methods to extract count and size of photos/videos for each month


class DateRange:
    def __init__(self, start=None, end=None, year=None, month=None):
        self.start = start
        self.end = end

        # handle string input by converting to integer
        if isinstance(year, str):
            year = int(year)

        if isinstance(month, str):
            month = utils.get_month_int(month)

        if year is not None and month is not None:
            self.set_start_end_from_yr_mo(year, month)

    def set_start_end_from_yr_mo(self, year, month):
        self.start = date(year, month, 1)

        days_in_month = self.get_days_from_month(year, month)
        self.end = date(year, month, days_in_month)

    def get_days_from_month(self, year, month):
        result = monthrange(year, month)
        return result[1]

    def is_in_date_range(self, a_date):
        if self.start <= a_date <= self.end:
            return True
        else:
            return False


# TODO: make photohistory class to encapsulate methods and printing options

print_enabled = False


def parse_types(types_dict):
    # given a dictionary of types, return a new dictionary of generalized types, based on what is being logged
    # e.g. jpg, JPG, jpeg are all Photo, so combine all those under photo
    types_dict = {}

    return types_dict


def get_file_size(file, unit=None):
    return round(convert_bytes(os.path.getsize(file), unit), 3)


def convert_bytes(size, unit='B'):
    factor = 1000 # non-binary conversion
    if unit == "B":
        return size
    elif unit == "KB":
        return size / factor
    elif unit == "MB":
        return size / (factor * factor)
    elif unit == "GB":
        return size / (factor * factor * factor)
    else:
        return size


def init_types(types):
    type_dict = {}
    for a_type in types:
        type_dict[a_type] = {}
        type_dict[a_type]['count'] = 0
        type_dict[a_type]['size'] = 0

    return type_dict


def increment_type_data(types_dict, a_type, file):
    types_dict[a_type]['count'] += 1
    types_dict[a_type]['size'] += get_file_size(file, 'MB')


def is_file_in_date_range(file, date_range):
    # TODO: need to get file date, creation date, compare that to date_range
    file_date = get_creation_date(file)
    return date_range.is_in_date_range(file_date)


def get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return datetime.fromtimestamp(os.path.getctime(path_to_file)).date()
    else:
        stat = os.stat(path_to_file)
        try:
            return datetime.fromtimestamp(stat.st_birthtime).date()
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return datetime.fromtimestamp(stat.st_mtime).date()


def get_types_from_folder(directory, date_range=None):

    # extensions
    photo_exts = utils.get_extensions_from_type('photo')
    video_exts = utils.get_extensions_from_type('video')
    live_photo_ext = utils.get_extensions_from_type('livephoto')
    live_photo_mov_ext = utils.get_extensions_from_type('livephotovideo')
    screenshot_exts = utils.get_extensions_from_type('screenshot')
    raw_exts = utils.get_extensions_from_type('raw')

    # find all photos
    num_photos_glob = 0
    for photo_ext in photo_exts:
        num_photos_glob += utils.get_num_files(directory, photo_ext)

    file_count = utils.get_num_files(directory, '.*')
    #print(utils.get_files_with_ext(directory, '.*'))

    # initialize count and size
    types_list = ['applephoto', 'livephoto', 'livephotovideo',
                  'video', 'photo',
                  'screenshot', 'raw',
                  'other']
    types_dict = init_types(types_list)
    #print(types_dict)

    # find all file types (count and size)
    files = Path(directory).rglob('**/*.*') # option to get all files recursively or not
    for file in files:

        # filter out any file that is outside date range
        if date_range is not None and not is_file_in_date_range(file, date_range):
            continue

        # because path is object not string
        file_str = str(file)

        # ignore DS_Store files on mac
        if '.DS_Store' in file_str:
            continue

        # get type, count, size
        if print_enabled:
            print(file_str)

        if any(ext in file_str for ext in live_photo_ext):
            # Live Photo
            increment_type_data(types_dict, 'livephoto', file)

        elif any(ext in file_str for ext in live_photo_mov_ext):
            # Live Photo videos
            increment_type_data(types_dict, 'livephotovideo', file)

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
                if print_enabled:
                    print('Found photo taken from Apple device')
            else:
                photo_type = 'photo'

            increment_type_data(types_dict, photo_type, file)

        elif any(ext in file_str for ext in video_exts):
            # Video
            increment_type_data(types_dict, 'video', file)

        elif any(ext in file_str for ext in screenshot_exts):
            # Screenshots
            increment_type_data(types_dict, 'screenshot', file)

        elif any(ext in file_str for ext in raw_exts):
            # Raw photos
            increment_type_data(types_dict, 'raw', file)

        else:
            # Other files
            increment_type_data(types_dict, 'other', file)

    # verify count of all photos, otherwise exit
    #print(types_dict['applephoto']['count'])
    #print(types_dict['photo']['count'])
    #print(types_dict['livephoto']['count'])
    #print(num_photos_glob)
    # TODO: This isn't always true when including the heic photos
    #assert types_dict['applephoto']['count'] + types_dict['photo']['count'] + types_dict['livephoto']['count'] == num_photos_glob

    # verify that all files have been counted and sized
    file_counter = 0
    for type, data in types_dict.items():
        file_counter += data['count']
    print('Total files found: {}'.format(file_counter))
    if not date_range:
        assert file_count == file_counter
        print('All files have been counted and sized')

    return types_dict


def get_sheet_by_name(book, name):
    """Get a sheet by name from xlwt.Workbook, a strangely missing method.
    Returns None if no sheet with the given name is present.
    """
    # Note, we have to use exceptions for flow control because the
    # xlwt API is broken and gives us no other choice.
    try:
        for idx in itertools.count():
            sheet = book.get_sheet(idx)
            if sheet.name == name:
                return sheet
    except IndexError:
        return None


def write_excel(types_dict, existing_file=False, offset=0, filename='types_data.xls', sheetname='Sheet 1'):

    if existing_file:
        rb = open_workbook(filename)

        #sheet1 = rb.sheet_by_name(sheetname)
        wb = copy(rb)
        sheet1 = get_sheet_by_name(wb, sheetname)
        #sheet.write(5, 2, "string")
        #wb.save('my_workbook.xls')

    else:
        # Workbook is created
        wb = Workbook()

        # add_sheet is used to create sheet.
        sheet1 = wb.add_sheet(sheetname)

    iter = 0
    for a_type, value in types_dict.items():
        sheet1.write(0, iter, a_type + '_count')
        sheet1.write(offset+1, iter, types_dict[a_type]['count'])
        iter += 1
        sheet1.write(0, iter, a_type + '_size')
        sheet1.write(offset+1, iter, types_dict[a_type]['size'])
        iter += 1

    wb.save(filename)


if __name__ == '__main__':

    # TODO: Read from excel file and choose to add to values that already exist there
    # TODO: Have one excel to read from and a different one to write to, to preserve data
    # TODO: Description column just with the directory
    # TODO: Way to automate all the folders, since this only works for one right now.
    # TODO: Come up with format of excel file for several folders, probably just rows for each unique subdirectory
    # TODO: Incorporate some logic based on the date. Need a way to only log ones for a particular month/year
    # TODO: Write tests for photohistory, including date range filtering
    # TODO: Have a sheet for each month/year or something?
    # TODO: Start with the Exported Photo Library, because month/year is easy by folder

    mode = 'single'

    if mode == 'single':
        directory1 = '/Users/sammcdonald/Documents/photos'
        #directory1 = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2020/01 January'
        directory1 = 'files/identical/dir1'
        date_range = DateRange(year=2020, month='January')
        #date_range=None
        types_dict = get_types_from_folder(directory1, date_range=date_range)
        print(types_dict)

        write_excel(types_dict)
    elif mode == 'exportedphotolibrary':
        year_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2020'

        month_dirs = [x[0] for x in os.walk(year_dir)]
        month_idx = 0
        for month_dir in month_dirs:
            if month_dir == year_dir:
                continue
            print(month_dir)
            types_dict = get_types_from_folder(month_dir)
            write_excel(types_dict, existing_file=True, offset=month_idx)
            month_idx += 1

