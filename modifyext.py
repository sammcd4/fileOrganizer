# Change extensions to all files in a given folder
import os, sys


def modify_exts(directory):

    extensions = {
        '.JPG': '.jpeg',
        '.MOV': '.mov',
        '.PNG': '.png',
        '.HEIC': '.heic',
        '.CR2': '.cr2',
        '.AAE': '.aae'
    }

    if False:
        extensions = {
            '.MOV': '.mov'
        }


    # only renames on one folder level
    for filename in os.listdir(directory):
        filepath = os.path.join(directory,filename)
        if not os.path.isfile(filepath): continue
        oldbase = os.path.splitext(filename)

        # rename file for each extension pair
        for old_ext in extensions:
            convert_to_lower = True
            if convert_to_lower:
                if not old_ext in filepath: continue
                new_path = filepath.replace(old_ext, extensions[old_ext])
            else:
                if not extensions[old_ext] in filepath: continue
                new_path = filepath.replace(extensions[old_ext], old_ext)
            output = os.rename(filepath, new_path)
            print('Rename file:\n\t{}\n\t{}'.format(filepath, new_path))


if __name__ == '__main__':
    directory = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2019/11_12 November'
    modify_exts(directory)