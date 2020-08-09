import os
import glob


def get_num_files(directory, ext):
    # use glob.glob to search for files with the specified extension
    return len(get_files_with_ext(directory, ext))


def get_files_with_ext(directory, ext):
    # use glob.glob to search for files with the specified extension
    return glob.glob(directory + '/**/*' + ext, recursive=True)


def get_extensions(directory):
    # return a list of all file extensions in this directory
    exts = []
    return exts


def get_convertible_extensions(extension):
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
    else:
        return []


def modifyextensions(directory, extensions, reverse_conversion=False):

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


def oldPhotosExtensions(directory, reverse_conversion=True):
    extensions = {
        '.JPG': '.jpeg',
        '.MOV': '.mov',
        '.PNG': '.png',
        '.HEIC': '.heic',
        '.CR2': '.cr2',
        '.AAE': '.aae'
    }
    modifyextensions(directory, extensions, reverse_conversion)


def newPhotosExtensions(directory):
    oldPhotosExtensions(directory, False)


def movExtensions(directory):
    extensions = {
        '.MOV': '.mov'
    }
    modifyextensions(directory, extensions)

def MOVExtensions(directory):
    extensions = {
        '.MOV': '.mov'
    }
    modifyextensions(directory, extensions, True)