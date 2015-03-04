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
        
        cmd = "INSERT INTO TeamStats({}) VALUES({});".format(columns, values)
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
        self.__addPlayer(playerStats[0], playerStats[1])

        self.cursor.execute(
            "SELECT * FROM {} WHERE week = {};".format(playerStats[0], date))
        if(len(self.cursor.fetchall()) == 0): 
            self.__addNewPlayerStats(playerStats, headers, date)
        else: 
            self.__updatePlayerStats(playerStats, headers, date)


    # __addPlayer()
    # called by addPlayerStats() each time it executes
    # checks to see if the player named is already listed.
    # if not, adds the player to the school's roster and creates a table 
    #   for the player's stats.
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


    #  __addNewPlayerStats()
    # called by addPlayerStats()
    def __addNewPlayerStats(self, stats, headers, date):
        columns = "week"
        values = date

        for i in range(2, len(headers)):
            columns += ", " + headers[i]
            if(playerStats[headers[i]] == 'TEXT'):
                values += ", '" + stats[i] + "'"
            elif( type(stats[i]) is tuple):
                for s in stats[i]: values += ", " + s
            else: values += ", " + stats[i]
            
        cmd = "INSERT INTO {}({}) VALUES ({})".format(stats[0], columns, values)
        self.cursor.execute(cmd)


    # __updatePlayerStats()
    # called by addPlayerStats() if a player already exists
    def __updatePlayerStats(self, stats, headers, date):
        cmd = "UPDATE {} \n".format(stats[0])
        cmd += "SET {} = {}".format(headers[2], stats[2])
        
        for i in range(3, len(stats)):  
            if(playerStats[headers[i]] == 'TEXT'):
                cmd += ", {} = '{}'".format(headers[i], stats[i])   
            else:
                cmd += ", {} = {}".format(headers[i], stats[i])
        cmd += "\n WHERE week = {};".format(date)
        self.cursor.execute(cmd)
        
            
            
    # __createPlayerStatsTable()
    # called by __addPlayer() to initialize the table named for the player,
    # consisting of all of their stats keyed by week            
    def __createPlayerStatsTable(self, player):
        try: self.cursor.execute( "SELECT * FROM {};".format(player))
        except:
            cmd = "CREATE TABLE " + player + "("        
            fields = playerStats.items()
            for (name, value) in fields:
                cmd +=  name + " " + value + ", \n"
            
            cmd += "PRIMARY KEY (week));"            
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
        
        
