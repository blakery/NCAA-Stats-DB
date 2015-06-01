"""
process ncaa basketball stats from a csv file
"""
import csv
import re
import statsdb
import sys
import os


def convert_date(old_date):
    """convert the date from the format NCAA uses to one acceptable to mysql
    In the NCAA files, it's month/day/year: We need it to be Year/Month/Day
    """
    temp = re.findall(r'\d+', old_date)
    new_date = temp[2] + "/" + temp[0] + "/" + temp[1]
    return new_date


def get_date(csv_file):
    """return the first date encountered in a file"""
    buff = csv_file.read()
    date = re.compile(r'\d+/\d+/\d+')
    return convert_date(re.search(date, buff).group())


def format_data(row):
    """make sure all the elements are properly formatted"""
    final = []
    for element in row:
        if element == 'W-L':    # separate W-L and int - int into two elements
            final.append('W')
            final.append('L')
        elif re.match(r'\d+-\d+', element): # separate int-int as well
            final.extend(re.findall(r'\d+', element))
        elif element == 'NR':    # Standing for "Not Ranked". It's irrelevant.
            final.append('')
        elif re.match(r'\d+\.\d+', element):    # don't replace decimal points
            final.append(element)
        else:                    # get rid of any other troublesome characters
            def elem_repl(match):
                """simple replacement function to call in re.sub()"""
                if match.group(0) == ' ':
                    return '_'
                elif match.group(0) == '%':
                    return '_PERCENTAGE'
                elif match.group(0) == '&':
                    return '_and_'
                else:
                    return ''
            final.append(re.sub(r"[. ')(&%-]", elem_repl, element))
    return final


def read_stats(reader):
    """read from a csv reader, and return a list of the stats"""
    rows = []
    for row in reader:
        if len(row) > 1:     # anything < length 1 is junk courtesy of NCAA
            rows.append(format_data(row))
    return rows


def process_stats(rows, date, database):
    """called to process a list of stats"""
    i = 1
    while i < (len(rows)-1) and rows[i][0] != 'Rank':
        i += 1
    if i == 1:
        return                 # didn't go anywhere - probably empty list
    elif rows[i][0] == "Rank": # still have another block after this
        database.process_block(rows[:(i-1)], date)
        process_stats(rows[i:], date, database)
    else:
        database.process_block(rows, date)


def process_csv_file(csvfile):
    """read and process ncaa basketball stats from a csv file"""
    database = statsdb.StatsDBInput()

    with open(csvfile) as infile:
        date = get_date(infile)

        infile.seek(0)
        reader = csv.reader(infile)
        rows = read_stats(reader)
        process_stats(rows, date, database)



def is_ncaa_stat_file(filepath):
    """
    check to see if the file is an ncaa stat file.
    right now it just checks for the csv extension
    """
    _, ext = os.path.splitext(filepath)
    return ext == '.csv'


def iterate_directory(path):
    """run through all the entries in path and process the csv files"""
    for dirpath, _, files in os.walk(path):
        for filepath in files:
            if is_ncaa_stat_file(filepath):
                process_csv_file(os.path.join(dirpath, filepath))


def process(filepath):
    """main entry point for a string that is a filename or dirname"""
    if os.path.isdir(filepath):
        iterate_directory(filepath)
    elif is_ncaa_stat_file(filepath):
        process_csv_file(filepath)
    else: print "unrecognized file type"




if __name__ == "__main__":
    if len(sys.argv) > 1:
        process(sys.argv[1])

