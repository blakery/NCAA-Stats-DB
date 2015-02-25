import MySQLdb
from StatsHeaders import *


class StatsDB:

    """
    Class for adding entries to the stats database in the form 
    given by the parser
    
    
    Attributes:
        db -- database connection returned by MySQLdb.connect()
        cursor -- cursor object returned by db.connect()

    The database contains the following unique tables:
        * a label of "stats" indicates multiple values, 
            which are found in more detail in StatsHeaders.py
                    
                |------------|   
                |   teams    |
                |------------|
                | name TEXT  |
                |------------|

                |-------------------------------|
                |           TeamStats           |
                |-------------------------------|
                | name TEXT | week DATE | stats | 
                |-------------------------------|

    In addition, the database contains the following non-unique tables:
                
        For each team:
            |------------------------------------|
            |           [team name]              |
            |------------------------------------|
            | player name | ht DECIMAL | yrs 1-4 |
            |------------------------------------|
            * the method of storing the years the player has played for
              the team is still uncertain
    

        For each player:
            |-------------------------------|
            |         [player name]         |
            |-------------------------------|
            | team TEXT | week DATE | stats |
            |-------------------------------|
    
    
    """




    def __init__(self, host="localhost", user="blake", 
                 password="", db="BracketStats"):
        if(db == ""):
            self.db = MySQLdb.connect(host=host, user=user, passwd=password)
        else:
            self.db = MySQLdb.connect(host=host, user=user, 
                passwd=password, db=db)
        self.cursor = self.db.cursor()
        
#        self.createTeamsTable()
#        self.createTeamStatsTable()
#        self.createPlayerStatsTable()

        

    def processBlock(self, block, date):
        
        header = block[0]
        # player stats always have "Team" as the name of the 3rd column;
        # team stats do not
        # exclude the first column, the numerical ranking, as it's 
        #   a. a derived statistic, and 
        #   b. too variable and inconsitant to be of any use.
        if(header[2] == 'Team'): 
            for player in block[1:]:                
                self.addPlayerStats(player[1:], header[1:], date)
        else:
            for team in block[1:]:
                self.addTeamStats(team[1:], header[1:], date)



    # teamStats is a list consisting of: [team name, stats...]
    def addTeamStats(self, stats, headers, date):
        self.__addTeam(stats[0])
        
        columns = "week" 
        values = date

        for i in range(len(headers)):
            columns += ", " + headers[i]
            if(teamStats[headers[i]] == 'TEXT'):
                values += ", '{}'".format(stats[i])
            else: values += ", " + stats[i]
        #for h in headers[1:]:
        #    columns += ", " + h
            # currently, the parser breaks "W-L" down into "W" "L"already, 
            # but this way, changing that won't cause problems
           # if(h == "W-L"): columns += ", W, L"
           # else: columns += ", " + h 
        #for v in teamStats[1:]:
#            if v is 
         #   values += ", " + v
            # corresponding to the above "W-L" schenario
           # if(type(v) is tuple): values += ", " + v[0] + ", " + v[1]
          #  else: values += ", " + v

        cmd = "INSERT INTO TeamStats({}) VALUES({});".format(columns, values)
      #  print(cmd)
        self.cursor.execute(cmd)

        
    def __addTeam(self, school):
        self.cursor.execute(
            "SELECT * FROM teams WHERE name = '{}';".format(school))
        if(len(self.cursor.fetchall()) == 0): 
            self.cursor.execute(
                "INSERT INTO teams (name) VALUES ('{}');".format(school))
            self.__createTeamRosterTable(school)
        else: pass


    def __createTeamRosterTable(self, school):
        self.cursor.execute(
            "CREATE TABLE {}(player TEXT, ht DECIMAL);".format(school))




    # playerStats is a list in the form of [name, school, stats...]
    # headers is a list of the corresponding column names
    def addPlayerStats(self, playerStats, headers, date):    
        #self._addTeam(playerStats[1])
        self.__addPlayer(playerStats[0], playerStats[1])

        self.cursor.execute(
            "SELECT * FROM {} WHERE week = {};".format(playerStats[0], date))
        if(len(self.cursor.fetchall()) == 0): 
            self.__addNewPlayerStats(playerStats, headers, date)
        else: 
            self.__updatePlayerStats(playerStats, headers, date)



    def __addPlayer(self, player, school):
        self.__addTeam(school)
        self.cursor.execute("SELECT * FROM {} \
            WHERE player = '{}';".format(school, player))
        if(len(self.cursor.fetchall()) == 0):
            self.cursor.execute(
                "INSERT INTO {}(player) VALUES('{}');".
                format(school, player))
            self.__createPlayerStatsTable(player)
            self.db.commit()        
        else: pass  



    def __addNewPlayerStats(self, playerStats, headers, date):
            
        # FIXME currently yr will be listed as a stat. 
        #       the headers should be checked, and yr should be skipped.
        #       also need to check for tuples in player stats...?
        # FIXME: will not handle 'TEXT' properly! see addTeamStats()
        columns = "week"
        for h in headers[2:]:
            columns += ", " + h

        values = date
        for s in playerStats[2:]: 
            values += ", " + s
        cmd = "INSERT INTO {}({}) VALUES ({})".format(playerStats[0], 
            columns, values)        
        self.cursor.execute(cmd)


    def __updatePlayerStats(self, playerStats, headers, date):
            
        # FIXME currently yr will be listed as a stat. 
        #       the headers should be checked, and yr should be skipped.
        #       also need to check for tuples in player stats...?
        cmd = "UPDATE {}\n".format(playerStats[0])
        cmd += "SET {} = {},".format(headers[2], playerStats[2])
        
        for i in range(3, len(playerStats)):
            cmd += ", {} = {}".format(headers[i], playerStats[i])
        cmd += "\nWHERE week = {};".format(date)
        self.cursor.execute(cmd)
        
            
            
                
   
  

    def __createPlayerStatsTable(self, player):
        try: self.cursor.execute( "SELECT * FROM {};".format(player))
        except:
            cmd = "CREATE TABLE " + player + "("        
            fields = playerStats.items()
            for (name, value) in fields:
                cmd +=  name + " " + value + ", \n"
            
            cmd += "PRIMARY KEY (week));"
           # print(cmd)
            
            self.cursor.execute(cmd) 
        
        





    """ Methods for creating unique tables:
          -- createTeamsTable()
          -- createTeamStatsTable()

    """

    def createTeamsTable(self):
        try: self.cursor.execute( "SELECT * FROM teams;")
        except: 
            self.cursor.execute("CREATE TABLE teams(name TEXT);")
            self.db.commit()
            

    def createTeamStatsTable(self):
        try: self.cursor.execute( "SELECT * FROM TeamStats;")
        except:
            cmd = "CREATE TABLE TeamStats("
        
            fields = teamStats.items()
            cmd += fields[0][0] + " " + fields[0][1]
            for (name, value) in fields[1:]:
                cmd += ", " + name + " " + value
            cmd += ");"
            self.cursor.execute(cmd)



    
    # a wrapper for cursor.execute(), used primarily for tests. 
    # this may go away at some point
    def execute(self, cmd):
        self.cursor.execute(cmd)
        
        
