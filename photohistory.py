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

print_enabled = True


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
    file_date = utils.get_creation_date(file)
    return date_range.is_in_date_range(file_date)


def get_types_from_folder(directory, date_range=None, drill_down=True, init_file=None, init_row_idx=1, init_sheetname='Sheet 1'):
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
                  'applevideo', 'screenshot',
                  'photo', 'raw', 'video',
                  'other']
    types_dict = init_types(types_list)

    if init_file:
        # read in file and set data of types_dict to data in file
        rb = open_workbook(init_file)
        sheet1 = rb.sheet_by_name(init_sheetname)
        sheet1 = rb.sheet_by_index(0)

        # iterate through first row's values, which should be the keys of types_dict
        col = 0
        title = sheet1.cell_value(0, col)
        while title:
            if '_' in title:
                type_key = title.split('_')[0]
                val_type = title.split('_')[1]
                if type_key in types_dict.keys():
                    type_val = sheet1.cell_value(init_row_idx, col)
                    if not isinstance(type_val, str):
                        types_dict[type_key][val_type] = type_val
            col += 1
            try:
                title = sheet1.cell_value(0, col)
            except:
                title = None

    #print(types_dict)

    # find all file types (count and size)
    if drill_down:
        file_spec = '**/*.*'
        files = Path(directory).rglob(file_spec)
    else:
        file_spec = '*.*'
        files = Path(directory).glob(file_spec)

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
    if not date_range and not init_file:
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


def write_excel(types_dict, directory_name=None, existing_file=False, offset=0, filename='types_data.xls', sheetname='Sheet 1'):

    if existing_file:
        # TODO: allow to read multiple sheets instead of only one

        # if it doesn't exist yet, create it, so that it can be used iteratively
        if not os.path.isfile(filename):
            wb = Workbook()
            sheet1 = wb.add_sheet(sheetname)
            wb.save(filename)

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

    # initialize column index
    iter = 0

    # if supplied, write folder name to first column
    if directory_name:
        sheet1.write(0, iter, 'directory')
        sheet1.write(offset + 1, iter, directory_name)
        iter += 1

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
    # TODO: Way to automate all the folders, since this only works for one right now.
    # TODO: Come up with format of excel file for several folders, probably just rows for each unique subdirectory
    # TODO: Incorporate some logic based on the date. Need a way to only log ones for a particular month/year
    # TODO: Write tests for photohistory, including date range filtering
    # TODO: Have a sheet for each month/year or something?

    mode = 'multiple'

    if mode == 'single':
        #directory1 = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/2019'
        directory1 = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/2019/2019_11'
        #directory1 = 'files/identical/dir1'
        date_range = DateRange(year=2019, month='December')
        #date_range=None
        types_dict = get_types_from_folder(directory1, date_range=date_range, drill_down=True)
        print(types_dict)

        write_excel(types_dict)
    elif mode == 'init_file':
        directory1 = '/Users/sammcdonald/Documents/empty'
        types_dict = get_types_from_folder(directory1, init_file='types_init.xls', init_row_idx=1)
        print(types_dict)

    elif mode == 'exportedphotolibrary':
        year = '2016'
        year_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/'+year

        month_dirs = [x[0] for x in os.walk(year_dir)]
        month_idx = 0
        for month_dir in month_dirs:
            if month_dir == year_dir:
                continue
            print(month_dir)
            types_dict = get_types_from_folder(month_dir)
            write_excel(types_dict, directory_name=month_dir, existing_file=True, offset=month_idx, filename='init_file_'+year+'.xls')
            month_idx += 1
    elif mode == 'multiple':
        # specify the directory to calculate for all subdirectories
        year = '2016'
        directory = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/' + year

        # specify months to do
        month_names = utils.get_month_names()

        for month_name in month_names:
            # specify date range to search for
            date_range = None
            if True:
                date_range = DateRange(year=year, month=month_name)

            #sub_dirs = [x[0] for x in os.walk(directory)] # recursive
            dir_idx = 0
            for sub_dir in utils.get_sub_dirs(directory):
                if sub_dir == directory:
                    continue
                print(sub_dir)
                types_dict = get_types_from_folder(sub_dir, date_range=date_range)
                write_excel(types_dict, directory_name=sub_dir, existing_file=True, offset=dir_idx, filename='types_'+month_name+'.xls')
                dir_idx += 1

    elif mode == 'multiple_months':
        # specify the directory to calculate for all months in a year
        year = '2015'
        directory = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/' + year
        #directory = '/Users/sammcdonald/Documents/empty'

        # specify months to do
        month_names = utils.get_month_names()

        month_idx = 0
        for month_name in month_names:
            # specify date range to search for
            date_range = None
            if True:
                date_range = DateRange(year=year, month=month_name)

            types_dict = get_types_from_folder(directory, date_range=date_range) # init_file='init_file_'+year+'.xls', init_row_idx=month_idx+1)
            write_excel(types_dict, directory_name=month_name, existing_file=True, offset=month_idx,
                        filename='types_'+year+'.xls')
            month_idx += 1

