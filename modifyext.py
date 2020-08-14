# Change extensions to all files in a given folder
import fileorganizer.utils as utils


def modify_exts(directory):

    extensions = {
        '.JPG': '.jpeg',
        '.MOV': '.mov',
        '.PNG': '.png',
        '.HEIC': '.heic',
        '.CR2': '.cr2',
        '.AAE': '.aae'
    }

    utils.modify_extensions(directory, extensions, True)
    #utils.old_photos_extensions(directory)
    #utils.mov_extensions(directory)


if __name__ == '__main__':
    directory = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/Screenshots/Workout'
    modify_exts(directory)
