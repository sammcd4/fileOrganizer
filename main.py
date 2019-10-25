import fileorganizer as fo
import fileorganizer.comparator as fo_c

mode = 'compare'
dir1 = '/Volumes/Seagate 4/Seagate 2 Backup/_gsdata_/_saved_/Photos + Videos/Exported Photo Library/2019/09_19 September'
dir2 = '/Volumes/Seagate 2/Photos + Videos/Exported Photo Library/2019/09 September'

comp = fo_c.Comparator()
comp.compare_folders(dir1, dir2)
