"""
process ncaa basketball stats from a csv file
"""
import csv
import sys
import re
import statsdb


def convert_date(old_date):
    """convert the date from the format NCAA uses to one acceptable to mysql
    In the NCAA files, it's month/day/year: We need it to be Year/Month/Day
    """
    temp = re.findall(r'\d+', old_date)
    new_date = "'" + temp[2] + "/" + temp[0] + "/" + temp[1] + "'"
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
        if element == 'W-L':# separate W-L and int - int into two elements
            final.append('W')
            final.append('L')
        elif re.match(r'\d+-\d+', element):
            final.extend(re.findall(r'\d+', element))
        elif element == 'NR':
            final.append('')
        elif re.match(r'\d+\.\d+', element): #don't replace decimal points
            final.append(element)
        else: # get rid of any other troublesome characters
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
        if len(row) > 1: # anything < length 1 is junk courtesy of NCAA
            rows.append(format_data(row))
    return rows


def process_stats(rows, date, database):
    """called to process a list of stats"""
    i = 1
    while i < (len(rows)-1) and rows[i][0] != 'Rank':
        i += 1
    if i == 1:
        return # didn't go anywhere - probably empty list
    elif rows[i][0] == "Rank": # still have another block after this
        database.process_block(rows[:(i-1)], date)
        process_stats(rows[i:], date, database)
    else:
        database.process_block(rows, date)


def process_csv_file(csvfile):
    """read and process ncaa basketball stats from a csv file"""
    database = statsdb.StatsDB()

    with open(csvfile) as infile:
        date = get_date(infile)

        infile.seek(0)
        reader = csv.reader(infile)
        rows = read_stats(reader)
        process_stats(rows, date, database)



if __name__ == "__main__":
    process_csv_file(sys.argv[1])
