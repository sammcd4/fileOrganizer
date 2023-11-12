#!/bin/bash

# Basic backup script and keep any deleted files from source

dry_run=""
verbose=0
deleted_backup_dir="../recently_deleted_files/"

Help()
{
   # Display Help
   echo "Backup SRC (first argument) to DEST (second argument) and keep any deleted files from SRC"
   echo
   echo "Syntax: backup [-h|d|v] <SRC> <DEST>"
   echo "options:"
   echo "h     Print this Help."
   echo "n     Dry run only."
   echo "v     Verbose mode."
   echo
}

# Get the options
while getopts ":hnv" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      v) # enable verbose mode
         verbose=1
         ;;
      n) # use rsync dry run
         dry_run="-n"
         ;;
   esac
done
shift $((OPTIND - 1))

src=$1
dest=$2

if [ "$verbose" -eq 1 ]; then
    # Explanation of backup
    echo "Running backup script..."
    echo "SRC: $src"
    echo "DEST: $dest"
    echo "Deleted files backup directory relative to DEST: $deleted_backup_dir"
fi

# Check is correct arguments are supplied
if [ $# -eq 0 ]; then
    echo "No arguments supplied"
elif [ $# -eq 1 ]; then
    echo "Only 1 argument given. SRC=$src"
elif [ $# -eq 2 ]; then
    # Run backup command
    backup_cmd="rsync -a -v $dry_run --delete --backup --backup-dir=$deleted_backup_dir \"$src/\" \"$dest/\""
    if [ "$verbose" -eq 1 ]; then
        echo "Running command:"
        echo $backup_cmd
    fi
    eval $backup_cmd
fi