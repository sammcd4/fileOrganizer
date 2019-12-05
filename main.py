import fileorganizer as fo
import fileorganizer.comparator as fo_c

mode = 'compare'
dir1 = '/Volumes/Seagate 2/Photos + Videos/Exported Photo Library/2019/11_12 November'
dir2 = '/Volumes/Seagate 2/Photos + Videos/Exported Photo Library/2019/11 November'

comp = fo_c.Comparator()
comp.compare_folders(dir1, dir2)
