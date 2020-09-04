import os
import glob
import calendar


def get_month_int(month_str):
    str_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    name_to_num = {name: num for num, name in enumerate(calendar.month_name) if num}
    str_to_num.update(name_to_num) # merge dictionaries
    
    return str_to_num[month_str]


def get_month_folder_names():
    # TODO make this better
    return ['01 January',
            '02 February',
            '03 March',
            '04 April',
            '05 May',
            '06 June',
            '07 July',
            '08 August',
            '09 September',
            '10 October',
            '11 November',
            '12 December']


def get_num_files(directory, ext, recursive=True):
    # use glob.glob to search for files with the specified extension
    return len(get_files_with_ext(directory, ext, recursive))


def get_files_with_ext(directory, ext, recursive=True):
    # use glob.glob to search for files with the specified extension
    return glob.glob(str(directory) + '/**/*' + ext, recursive=recursive)


def get_extensions(directory):
    # return a list of all file extensions in this directory
    exts = []

    # Iterate over all files in the directory and append any new extensions
    files = get_files_with_ext(directory, '.*')
    for file in files:
        name, ext = os.path.splitext(file)
        if ext not in exts:
            exts.append(ext)
    return exts


def get_convertible_extensions(extension, prepend=None):
    # given a file extension, get a list of all similar extensions
    if extension == '.JPG':
        return ['.jpg', '.jpeg', '.JPEG']
    elif extension == '.jpg':
        return ['.JPG', '.jpeg', '.JPEG']
    elif extension == '.jpeg':
        return ['.JPG', '.jpg', '.JPEG']
    elif extension == '.JPEG':
        return ['.jpg', '.JPG', '.jpeg']
    elif extension == '.mov':
        return ['.MOV']
    elif extension == '.MOV':
        return ['.mov']
    elif extension == '.heic':
        return ['.HEIC']
    elif extension == '.HEIC':
        return ['.heic']
    elif extension == '.MPG':
        return ['.mpg', '.mpeg', '.MPEG']
    elif extension == '.mpg':
        return ['.MPG', '.mpeg', '.MPEG']
    elif extension == '.mpeg':
        return ['.mpg', '.MPG', '.MPEG']
    elif extension == '.MPEG':
        return ['.MPG', '.mpg', '.mpeg']
    elif extension == '.MP4':
        return ['.mp4']
    elif extension == '.mp4':
        return ['.MP4']
    elif extension == '.PNG':
        return ['.png']
    elif extension == '.png':
        return ['.PNG']
    elif extension.islower():
        return [extension.upper()]
    elif extension.isupper():
        return [extension.lower()]
    else:
        # mixed lower/upper case, so return both as convertible
        return [extension.lower(), extension.upper()]


def get_extensions_from_type(type):
    if type == 'photo':
        return get_extension_variations('.jpg')
    elif type == 'video':
        return get_extension_variations(['.mp4', '.mov', '.avi', '.mpg', '.m4v'])
    elif type == 'livephoto':
        return get_extension_variations(['.jpg', '.heic'], prepend_str='LivePhoto')
    elif type == 'livephotovideo':
        return get_extension_variations('.mov', prepend_str='LivePhoto')
    elif type == 'screenshot':
        return get_extension_variations('.png')
    elif type == 'raw':
        return get_extension_variations('.cr2')


def get_extension_variations(extension, prepend_str=None):
    if isinstance(extension, list):
        # for every extension, run the same algorithm and create list of all
        extensions = []
        for ext in extension:
            extensions.extend(get_extension_variations(ext))
    else:
        # implementation for a single extension
        extensions = [extension]
        extensions.extend(get_convertible_extensions(extension))

    if prepend_str is not None:
        extensions = [(prepend_str + '{0}').format(ext) for ext in extensions]

    return extensions


def modify_extensions(directory, extensions, reverse_conversion=False):

    if not os.path.isdir(directory):
        print('Non-existent directory: ', directory)
        return

    # TODO: Drill down on all folder levels
    # only renames on one folder level
    for filename in os.listdir(directory):
        filepath = os.path.join(directory,filename)
        if not os.path.isfile(filepath): continue
        os.path.splitext(filename)

        # rename file for each extension pair
        for old_ext in extensions:
            if not reverse_conversion:
                if old_ext not in filepath: continue
                new_path = filepath.replace(old_ext, extensions[old_ext])
            else:
                if extensions[old_ext] not in filepath: continue
                new_path = filepath.replace(extensions[old_ext], old_ext)
            os.rename(filepath, new_path)
            print('Rename file:\n\t{}\n\t{}'.format(filepath, new_path))


def old_photos_extensions(directory, reverse_conversion=True):
    extensions = {
        '.JPG': '.jpeg',
        '.MOV': '.mov',
        '.PNG': '.png',
        '.HEIC': '.heic',
        '.CR2': '.cr2',
        '.AAE': '.aae'
    }
    modify_extensions(directory, extensions, reverse_conversion)


def new_photos_extensions(directory):
    old_photos_extensions(directory, False)


def mov_extensions(directory):
    extensions = {
        '.MOV': '.mov'
    }
    modify_extensions(directory, extensions)

def MOV_extensions(directory):
    extensions = {
        '.MOV': '.mov'
    }
    modify_extensions(directory, extensions, True)