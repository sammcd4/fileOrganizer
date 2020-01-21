import fileorganizer.comparator as foc

base_dir = '/Volumes/Seagate 4/Seagate 2 Backup/Photos + Videos/Exported Photo Library/2019'

mode = 'multiple'
if mode == 'single':
    months = ['07 July']

elif mode == 'multiple':
    months = ['01 January',
              '02 February',
              '03 March',
              '04 April',
              '05 May',
              '06 June',
              '07 July',
              '08 August',
              '09 September',
              '10 October',
              '11 November',
              '12 December']

foc.compare_legacy_to_latest(base_dir, months)

