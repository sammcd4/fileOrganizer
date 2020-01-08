import os


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