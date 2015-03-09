import StatsParser
import sys
import os


def isNCAAStatFile(filepath):
    root, ext = os.path.splitext(filepath)
    return ext == '.csv'
     

def iterate_directory(path):

    for dirpath, dirnames, files in os.walk(path):
        for f in files:
            if(isNCAAStatFile(f)): 
                try: data = open(os.path.join(dirpath,f), "r")
                except Exception, args: print(args) 
                else:
                    try: StatsParser.processFile(data)
                    except Exception, args: print(args)
                    finally: data.close()

    

def main(argv):

    for fp in argv[1:]:
        if(os.path.isdir(fp)): iterate_directory(fp)
        elif(isNCAAStatFile(fp)): 
            print("processing: " + fp)
            StatsParser.processFile(fp)
            print(fp + " complete")
        else: print("unrecognized input") #FIXME handle this more thoroughly






if __name__ == '__main__':
    main(sys.argv)
