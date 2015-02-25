import unittest
from StatsDB import *

class TestStatsDB(unittest.TestCase):

    """"
    Unit Tests for StatsDB 
    - Note: Using StatsDB Requires use of MySQL
     
    Attributes:
        sDB -- StatsDB
        
    """


    def __init__(self, argv):

        sql = MySQLdb.connect(host="localhost", user="blake", 
                passwd="", db="testDB")
        cursor = sql.cursor()
        try:
            cursor.execute("DROP DATABASE testDB;")
        except:
            pass 
        cursor.execute("CREATE DATABASE testDB;")            
        sql.commit()
        
        self.sDB = StatsDB(db="testDB")
        
        self.sDB.createTeamsTable()
        self.sDB.createTeamStatsTable()
        #self.sDB.createPlayerStatsTable()
        
        super(TestStatsDB, self).__init__(argv)
    




    # After a player is added, the following should be true:
    #       An entry for the player keyed by name should exist in the 
    #           roster of the player's team
    #       A table should exist named "[player-name]"


    # After a team is added, the following should be true:
    #       It's name should be present in the table named "teams"
    #       A table should exist named "[team-name]Roster"

    def test_addPlayerStats(self):
        player = ['bob', 'bobs_school', '2', '5'] 
        header = ['Name', 'Team', 'FGA', 'G']
        date = "02/11/1995"
        s = self.sDB
        
        s.addPlayerStats(player, header, date)
        
        s.execute("SELECT G FROM bob WHERE week = {};".format(date))
        self.assertTrue(s.cursor.fetchone()[0] == 5)
        s.execute("SELECT FGA FROM bob WHERE week = {};".format(date))
        self.assertTrue(s.cursor.fetchone()[0] == 2)
        s.execute("SELECT * from bobs_school WHERE player = 'bob';")
        self.assertTrue(s.cursor.fetchone()[0] == 'bob')
        
        
                
    def test_addTeamStats(self):
        team = ['teamx', "1.1"]
        header = ["Name", "PPG"]
        date = "02/11/1995"
        s = self.sDB
        
        s.addTeamStats(team, header, date)
        
        s.execute("SELECT PPG from TeamStats \
                   WHERE week = {} AND name = '{}';".format(date, team[0]))
        x = s.cursor.fetchone()[0]
        self.assertTrue(float(x) == 1.10)

        
        
        

if __name__ == '__main__':
    unittest.main()
