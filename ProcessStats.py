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


def process(fp):
    if(os.path.isdir(fp)): iterate_directory(fp)
    elif(isNCAAStatFile(fp)): 
        StatsParser.processFile(fp)
    else: print("unrecognized file type") #FIXME handle this more thoroughly   



def main(argv):
    for fp in argv[1:]:
        process(fp)
        






if __name__ == '__main__':
    main(sys.argv)
