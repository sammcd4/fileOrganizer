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

    utils.modifyextensions(directory, extensions, True)
    #utils.oldPhotosExtensions(directory)
    #utils.movExtensions(directory)


if __name__ == '__main__':
    directory = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/Screenshots/Workout'
    modify_exts(directory)