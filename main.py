import fileorganizer as fo
import fileorganizer.comparator as fo_c

mode = 'compare'
dir1 = '/Users/mcdonaldfamily/Documents/2019_10_Pictures from Joh'
dir2 = '/Volumes/Seagate 2/Photos + Videos/2019_10_Pictures from Joh'

comp = fo_c.Comparator()
comp.compare_folders(dir1, dir2)
