import fileorganizer as fo
import fileorganizer.comparator as fo_c

mode = 'compare'
dir1 = '/Users/mcdonaldfamily/Documents/music to delete copy 3'
dir2 = '/Users/mcdonaldfamily/Music/iTunes/iTunes Media/Music'

comp = fo_c.Comparator()
comp.compare_folders(dir1, dir2)
