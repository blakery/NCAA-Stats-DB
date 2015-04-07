"""
takes a string that is a filename or directory and send the apropriate files
to the csv_reader
"""
import csv_stats
import sys
import os


def is_ncaa_stat_file(filepath):
    """
    check to see if the file is an ncaa stat file.
    right now it just checks for the csv extension
    """
    root, ext = os.path.splitext(filepath)
    return ext == '.csv'


def iterate_directory(path):
    """run through all the entries in path and process the csv files"""
    for dirpath, dirnames, files in os.walk(path):
        for filepath in files:
            if is_ncaa_stat_file(filepath):
                csv_stats.process_csv_file(os.path.join(dirpath, filepath))


def process(filepath):
    """main entry point for a string that is a filename or dirname"""
    if os.path.isdir(filepath):
        iterate_directory(filepath)
    elif is_ncaa_stat_file(filepath):
        csv_stats.process_csv_file(filepath)
    else: print "unrecognized file type"




if __name__ == '__main__':
    process(sys.argv[1])
