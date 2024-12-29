#!/bin/bash

# Basic backup script and keep any deleted files from source

dry_run=""
verbose=0
deleted_backup_dirname="recently_deleted_files"

usage()
{
   # Display Help
   echo "Backup SRC (first argument) to DEST (second argument) and keep any deleted files from SRC"
   echo
   echo "Syntax: backup [-h|d|v] [-b <BACKUP_DIR>] <SRC> <DEST>"
   echo "options:"
   echo "h     Print this Help."
   echo "n     Dry run only."
   echo "v     Verbose mode."
   echo "b     Specify the directory to backup recently deleted files. Default is '../recently_deleted_files/'."
   echo
}

# Get the options
while getopts ":hnvb:" option; do
   case $option in
      h) # display usage
         usage
         exit;;
      v) # enable verbose mode
         verbose=1
         ;;
      n) # use rsync dry run
         dry_run="-n"
         ;;
      b) # specify the backup directory
         deleted_backup_dirname="$OPTARG"
         ;;
      \?) # invalid option
         echo "Error: Invalid option -$OPTARG" >&2
         usage
         exit 1
         ;;
      :) # option requires an argument
         echo "Error: Option -$OPTARG requires an argument." >&2
         usage
         exit 1
         ;;
   esac
done
shift $((OPTIND - 1))

src=$1
dest=$2
deleted_backup_dir="../$deleted_backup_dirname/"

if [ "$verbose" -eq 1 ]; then
    # Explanation of backup
    echo "Running backup script..."
    echo "SRC: $src"
    echo "DEST: $dest"
    echo "Deleted files backup directory relative to DEST: $deleted_backup_dir"
fi

# Check is correct arguments are supplied
if [ $# -eq 0 ]; then
    usage
elif [ $# -eq 1 ]; then
    echo "Only 1 argument given. SRC=$src"
    usage
elif [ $# -eq 2 ]; then
    # Run backup command
    backup_cmd="rsync -a -v $dry_run --delete --backup --backup-dir=$deleted_backup_dir \"$src/\" \"$dest/\""
    if [ "$verbose" -eq 1 ]; then
        echo "Running command:"
        echo $backup_cmd
    fi
    eval $backup_cmd
fi