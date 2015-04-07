"""


"""
import CSVStats
import sys
import os


def isNCAAStatFile(filepath):
    root, ext = os.path.splitext(filepath)
    return ext == '.csv'
    

def iterate_directory(path):

    for dirpath, dirnames, files in os.walk(path):
        for f in files:
            if(isNCAAStatFile(f)): 
                CSVStats.CSVStatsReader(os.path.join(dirpath,f))


def process(fp):
    if(os.path.isdir(fp)): iterate_directory(fp)
    elif(isNCAAStatFile(fp)): 
        CSVStats.CSVStatsReader(fp)
    else: print("unrecognized file type") #FIXME handle this more thoroughly   



def main(argv):
    for fp in argv[1:]:
        process(fp)
        



if __name__ == '__main__':
    main(sys.argv)
