"""
    statsdb - contains StatsDB, a class for adding lists of stats to the
    mysql database

    TODO: (maybe) switch to using MySQL Connector/Python. Advantages:
        works with python 2 and 3. 
        appears to be better maintained and the more cannonical choice at this
            point

    TODO: consider numerical keys and foreign keys

    FIXME: Use proper string formating to prevent sql injection

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

        For each team:
            |--------------------------------|
            |          [team name]           |
            |--------------------------------|
            | player name | week DATE | stats|
            |--------------------------------|

"""
import MySQLdb
import Config
import stats_headers
#import mysql.Connector


def translate_team_stats(stats, index, name):
    """
    called return the sql name and data type of the name as it's
    listed in the ncaa stats files
    """
    if stats[index] is None or stats[index] == '':
        return None
    elif name == 'TO':
        return ('TURNOVERS', stats[index])
    elif name == 'ORebs' or name == 'DRebs' or name == 'Opp_FT' \
        or name == 'FOPPPTS' or name == 'FFPPG':
        return None
    elif stats_headers.TEAM_STATS[name] == 'TEXT':
        return (name, "'{}'".format(stats[index]))
    else: return (name, stats[index])


def translate_player_stats(stats, index, name):
    """
    called return the sql name and data type of the name as it's
    listed in the ncaa stats files
    """

    if stats[index] is None or stats[index] == '':
        return None
    # For the truly broken or incomprehensible stuff, return None
    elif name == 'ORebs' or name == 'DRebs' or name == 'Dbl_Dbl' or \
        name == 'MP' or name == 'MPG' or name == 'Trpl_Dbl':
        return None
    elif name == 'Ht':
        height = stats.pop(index) + "." + stats[index]
        return (name, height)
    #'TO' is a reserved keyword in sql
    elif name == 'TO':
        return ('TURNOVERS', stats[index])
    elif stats_headers.PLAYER_STATS[name] == 'TEXT':
        return (name, "'{}'".format(stats[index]))
    else: return (name, stats[index])




class StatsDBInput(object):
    """
    Class for adding entries to the stats database in the form
    given by the parser

    Attributes:
        _db -- database connection returned by MySQLdb.connect()
        cursor -- cursor object returned by _db.connect()
    """

    def __init__(self, host=None, user=None,
                 password="", db=None):
        if host is None:
            host = Config.getSQLHost()
        if user is None:
            user = Config.getSQLUserName()
        if db is None:
            db = Config.getSQLDB()
        try:
            self._db = MySQLdb.connect(host=host, user=user,
                                       passwd=password, db=db)
        except MySQLdb.OperationalError, args:
            print args
        else:
            self.cursor = self._db.cursor()
            self._create_teams_table()
            self._create_team_stats_table()


    def process_block(self, block, date):
        """process a block of player or team stats"""
        if len(block) == 0:
            return
        header = block[0]
        # player stats always have "Team" as the name of the 3rd column;
        # team stats do not. exclude the first column, the numerical ranking
        if len(header) < 3:
            print "invalid header: " + str(header)
        elif header[2] == 'Team':
            for player in block[1:]:
                try:
                    self.add_player_stats(player[1:], header[1:], date)
                except MySQLdb.ProgrammingError, args:
                    print args
                except KeyError, args:
                    print "Key error: " + date + ": " + str(args)
        else:
            for team in block[1:]:
                try:
                    self.add_team_stats(team[1:], header[1:], date)
                except MySQLdb.ProgrammingError, args:
                    print str(args) + ": " + date
                    print header
                    print team
                except KeyError, args:
                    print "Key error: " + date + ": " + str(args)


    def add_team_stats(self, stats, headers, date):
        """
        add team statistics to the TeamStats table
        stats is a list consisting of: [team name, stats...]
        """
        self._add_team(stats[0])
        columns = "week"
        values = date

        for i in range(len(headers)):
            trans = translate_team_stats(stats, i, headers[i])
            if trans is None:
                pass
            else:
                field, val = trans
                columns += ", " + field
                values += ", " + val
        cmd = "INSERT INTO TeamStats({}) VALUES({});".format(columns, values)
        self.cursor.execute(cmd)


    def _add_team(self, school):
        """
        add appropiate entries and tables to the database for a new team:
            - creates a team roster table
            - adds the team to the teams table
        """
        self.cursor.execute(
            "SELECT * FROM teams WHERE name = '{}';".format(school))
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute(
                "INSERT INTO teams (name) VALUES ('{}');".format(school))

        try: self.cursor.execute("SELECT * FROM {};".format(school))
        except:
            fields = stats_headers.PLAYER_STATS.items()
            name, value = fields[0]
            field_names = name + " " + value
            for (name, value) in fields[1:]:
                field_names += ", \n" + name + " " + value
            self.cursor.execute(
                "CREATE TABLE {} ({});".
                format(school, field_names))
        else:
            return




    def add_player_stats(self, stats, headers, date):
        """
        Add player stats to the sql database
        stats is a list in the form of [name, school, stats...]
        headers is a list of the corresponding column names
        """
        name = stats[0]
        team = stats[1]
        self._add_team(team)
        cmd = "SELECT * FROM {} WHERE Name = '{}' AND Week = {};".format(team, name, date)
        self.cursor.execute(cmd)
            
        if len(self.cursor.fetchall()) == 0:
            self._add_new_player_stats(stats, headers, date)
        else:
            self._update_player_stats(stats, headers, date)



    def _add_new_player_stats(self, stats, headers, date):
        """called by add_player_stats() to add a new player """
        columns = "name, week"
        values = "'" + stats[0] + "'," + date

        for i in range(2, len(headers) -1):
            trans = translate_player_stats(stats, i, headers[i])
            if trans is None:
                pass
            else:
                field, val = trans
                columns += ", " + field
                values += ", " + val
        cmd = "INSERT INTO {}({}) VALUES ({})".format(stats[1], columns, values)
        self.cursor.execute(cmd)


    def _update_player_stats(self, stats, headers, date):
        """called by add_player_stats() to update an existing player"""

        cmd = "UPDATE {} \n".format(stats[1])

        # get a valid value to start
        index = 2
        trans = translate_player_stats(stats, index, headers[index])
        while trans is None:
            index += 1
            trans = translate_player_stats(stats, index, headers[index])

        field, val = trans
        cmd += "SET {} = {}".format(field, val)

        for i in range(index+1, len(headers) -1):
            trans = translate_player_stats(stats, i, headers[i])
            if trans is None:
                pass
            else:
                field, val = trans
                cmd += ", {} = {}".format(field, val)

        cmd += "\n WHERE name = '{}' AND week = {};".format(stats[0], date)
        self.cursor.execute(cmd)


    def _create_teams_table(self):
        """create the global teams table"""
        #FIXME: check if resource exists in a more sensible way (ie IF EXISTS)
        try:
            self.cursor.execute("SELECT * FROM teams;")
        except MySQLdb.Error:
            self.cursor.execute(
                "CREATE TABLE teams(name TEXT);")
        self._db.commit()


    def _create_team_stats_table(self):
        """create the global teamstats table"""
        try:
            self.cursor.execute("SELECT * FROM TeamStats;")
        except MySQLdb.Error:
            cmd = "CREATE TABLE TeamStats("
            fields = stats_headers.TEAM_STATS.items()
            cmd += fields[0][0] + " " + fields[0][1]
            for (name, value) in fields[1:]:
                cmd += ", " + name + " " + value
            cmd += ");"
            self.cursor.execute(cmd)



class StatsDBOutput(object):
    '''

    '''


    def __init__(self, host=None, user=None,
                 password="", db=None):
        if host is None:
            host = Config.getSQLHost()
        if user is None:
            user = Config.getSQLUserName()
        if db is None:
            db = Config.getSQLDB()
        try:
            self._db = MySQLdb.connect(host=host, user=user,
                                       passwd=password, db=db)
        except MySQLdb.OperationalError, args:
            print args
        else:
            self.cursor = self._db.cursor()


    def get_teams(self):
        '''
        returns a list of teams in the database
        '''
        cmd = "SELECT * FROM teams;"
        self.cursor.execute(cmd)
        teams = []
        for t in self.cursor.fetchall():
            teams.append(t[0])
        return teams


    def get_players(self, team, year):
        '''
        returns the roster of a team for a particular year as a list
        '''

        cmd = "SELECT * FROM " + team + " WHERE YEAR(Week) = '" + str(year) + "';"
        self.cursor.execute(cmd)
        players = []
        player_data = self.cursor.fetchall()
        desc = self.cursor.description
        i=0
        while(desc[i][0] != 'Name'):
            i += 1
        
        for p in player_data:
            players.append(p[i])
        return players



