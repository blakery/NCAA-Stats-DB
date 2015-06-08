import sys
import os


def set_stderr(err_file):
    """
    TODO: Set default error file
    TODO: open file from path
    """
    sys.stderr = err_file


def mysql_input_error(args, stats=None, headers=None, date=None, action=None):
    if action:
        print >> sys.stderr, "ERROR when {}:".format(action)
    print >> sys.stderr, args
    if date:
        print >> sys.stderr, date
    if stats:
        print >> sys.stderr, stats
    if headers:
        print >> sys.stderr, headers


def mysql_testing_error(args, info=None, action=None):
    '''
    Called if a MySQLdb exception is thrown during testing.
    This should NOT be used to indicate a simple failed test.
    Uses are for things such as failing to remove a test case.
    Info is additional info, such as the name or table in which the error
    occoured, and action is what was being attempted at the time. Usually the
    function name will sufice.
    '''
    if action:
        print >> sys.stderr, "Error when {}.".format(action)
    print >> sys.stderr, args
    if info:
        print >> sys.stderr, "Additional info: {}".format(info)


def missing_column(date, args):
    """
    Called on a key error.
    This is usually a missing column in one of the header dicts. The NCAA
    stats people change them at seemingly random intervals, so it's easy
    to miss one sometimes.
    """
    err = "Key Error: " + args + "\nColumn name probably missing from " + date
    print >> sys.stderr, err





