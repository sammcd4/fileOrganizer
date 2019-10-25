import fileorganizer as fo
import fileorganizer.comparator as fo_c

mode = 'compare'
dir1 = '/Volumes/Seagate 2/Photos + Videos/Exported Photo Library/2019/10_23 October'
dir2 = '/Volumes/Seagate 2/Photos + Videos/Exported Photo Library/2019/10 October'

comp = fo_c.Comparator()
comp.compare_folders(dir1, dir2)
