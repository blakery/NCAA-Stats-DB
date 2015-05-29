import sys
import os


def set_stderr(err_file):
    """
    TODO: Set default error file
    TODO: open file from path
    """
    sys.stderr = err_file


def mysql_input_error(args, stats=None, headers=None, date=None):
    print >> sys.stderr, args
    if date:
        print >> sys.stderr, date
    if stats:
        print >> sys.stderr, stats
    if headers:
        print >> sys.stderr, headers




def missing_column(date, args):
    """
    Called on a key error.
    This is usually a missing column in one of the header dicts. The NCAA
    stats people change them at seemingly random intervals, so it's easy
    to miss one sometimes.
    """
    err = "Key Error: " + args + "\nColumn name probably missing from " + date
    print >> sys.stderr, err





