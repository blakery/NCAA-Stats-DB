import StatsParser
import sys
import os


def isNCAAStatFile(filepath):
    return True

def iterate_directory(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if(isNCAAStatFile(f)): 
                try: StatsParser.processFile(f)
                except: pass #FIXME handle errors, print log, ect. 

    

def main(argv):

    #fp = "TeamRankings2012.csv"    
    for fp in argv[1:]:
        if(os.path.isdir(fp)): iterate_directory(fp)
        elif(isNCAAStatFile(fp)): 
            print("processing: " + fp)
            StatsParser.processFile(fp)
        else: print("unrecognized input") #FIXME handle this more thoroughly






if __name__ == '__main__':
    main(sys.argv)
