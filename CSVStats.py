import csv
import sys
import os
import re
import StatsDB


class CSVStatsReader:

    def __init__(self, csvfile):
        self.db = StatsDB.StatsDB()
        
        with open(csvfile) as f:
            self.date = self.convertDate(self.getDate(f))

            f.seek(0)       
            reader = csv.reader(open(csvfile))
            rows = self.readStats(reader)
            self.processStats(rows)



    # convert the date from the format NCAA uses to one acceptable to mysql
    # In the NCAA files, it's month/day/year
    # We need it to be Year/Month/Day    
    def convertDate(self, oldDate):
        temp = re.findall(r'\d+', oldDate)
        newDate = "'" + temp[2] + "/" + temp[0] + "/" + temp[1] + "'"
        return newDate



    def getDate(self, csvfile):
        buff = csvfile.read()
        date = re.compile(r'\d+/\d+/\d+')
        return re.search(date, buff).group() 


    def readStats(self, reader):
        rows = []
        for row in reader: 
            # anything that is < length 1 is junk courtesy of NCAA
            if len(row) > 1:
                rows.append(self.formatData(row))
        return rows

    
    def formatData(self, row):
        final = []
        for element in row:
            # for W-L and int - int, separate into two elements
            if element == 'W-L':
                final.append('W')
                final.append('L')
            elif re.match(r'\d+-\d+', element):
                final.extend(re.findall(r'\d+', element))
            elif element == 'NR': final.append('')
            # don't replace decimal points
            elif re.match(r'\d+\.\d+', element): final.append(element)
            # get rid of any other troublesome characters
            else: 
                def elemRepl(match):
                    if match.group(0) == ' ': return '_'
                    elif match.group(0) == '%': return '_PERCENTAGE'
                    elif match.group(0) == '&': return '_and_'
                    else: return ''
                final.append( re.sub(r"[. ')(&%-]",elemRepl, element) )
        return final


    
    def processStats(self, rows):
        i=1
        while i < (len(rows)-1) and rows[i][0] != 'Rank': i+=1
        if i==1 : return            #didn't go anywhere - probably empty list
        elif rows[i][0] == "Rank":  #still have another block after this
            self.db.processBlock(rows[:(i-1)], self.date)        
            self.processStats(rows[i:])
        else: 
            self.db.processBlock(rows, self.date)        
            
            
        
        
        
        
        
if __name__ == "__main__":
    f = sys.argv[1]
    c = CSVStatsReader(f)
