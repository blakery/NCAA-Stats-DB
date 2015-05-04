"""
    statsdb - contains StatsDB, a class for adding lists of stats to the
    mysql database

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
import MySQLdb
import Config
import stats_headers



def translate_team_stats(stats, index, name):
    """
    called return the sql name and data type of the name as it's
    listed in the ncaa stats files
    """
    stat_val = stats[index]
    if stat_val is None or stat_val == '':
        return None
    elif name == 'TO':
        return ('TURNOVERS', stat_val)
    elif name == 'ORebs' or name == 'DRebs' or name == 'Opp_FT' \
        or name == 'FOPPPTS' or name == 'FFPPG':
        return None
    elif stats_headers.TEAM_STATS[name] == 'TEXT':
        return (name, "'{}'".format(stat_val))
    else: return (name, stat_val)


def translate_player_stats(stats, index, name):
    """
    called return the sql name and data type of the name as it's
    listed in the ncaa stats files
    """
    stat_val = stats[index]
    if stat_val is None or stat_val == '':
        return None
    elif name == 'Ht':
        return (name, stat_val + "." + stats.pop(index + 1))
    elif name == 'TO':              #'TO' is a reserved keyword in sql
        return ('TURNOVERS', stats[index])
    # For the truly broken or incomprehensible stuff, return None
    elif name == 'ORebs' or name == 'DRebs' or name == 'Dbl_Dbl' or \
        name == 'MP' or name == 'MPG' or name == 'Trpl_Dbl':
        return None
    elif stats_headers.PLAYER_STATS[name] == 'TEXT':
        return (name, "'{}'".format(stat_val))
    else: return (name, stat_val)




class StatsDB(object):
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
                    print args + ": " + date
                    print header
                    print player
                except KeyError, args:
                    print "Key error: " + date + ": " + str(args)
        else:
            for team in block[1:]:
                try:
                    self.add_team_stats(team[1:], header[1:], date)
                except MySQLdb.ProgrammingError, args:
                    print args + ": " + date
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
            self._create_team_roster_table(school)
        else: pass

    def _create_team_roster_table(self, school):
        """create the roster table for the team passed as 'school'"""
        self.cursor.execute(
            "CREATE TABLE {}(player TEXT, ht DECIMAL(6, 2));".format(school))



    def add_player_stats(self, stats, headers, date):
        """
        Add player stats to the sql database
        stats is a list in the form of [name, school, stats...]
        headers is a list of the corresponding column names
        """
        self._add_team(stats[1])
        self._create_player_stats_table(stats[0])
        self.cursor.execute(
            "SELECT * FROM {} WHERE week = {};".format(stats[0], date))
        if len(self.cursor.fetchall()) == 0:
            self._add_new_player_stats(stats, headers, date)
        else:
            self._update_player_stats(stats, headers, date)



    def _add_new_player_stats(self, stats, headers, date):
        """called by add_player_stats() to add a new player """
        columns = "week"
        values = date

        for i in range(2, len(headers) -1):
            trans = translate_player_stats(stats, i, headers[i])
            if trans is None:
                pass
            else:
                field, val = trans
                columns += ", " + field
                values += ", " + val
        cmd = "INSERT INTO {}({}) VALUES ({})".format(stats[0], columns, values)
        self.cursor.execute(cmd)


    def _update_player_stats(self, stats, headers, date):
        """called by add_player_stats() to update an existing player"""

        cmd = "UPDATE {} \n".format(stats[0])

        # get a valid value to start
        trans = translate_player_stats(stats, 2, headers[2])
        while trans is None:
            headers = headers[1:]
            stats = stats[1:]
            trans = translate_player_stats(stats, 2, headers[2])

        field, val = trans
        cmd += "SET {} = {}".format(field, val)

        for i in range(2, len(stats) -1):
            trans = translate_player_stats(stats, i, headers[i])
            if trans is None:
                pass
            else:
                field, val = trans
                cmd += ", {} = {}".format(field, val)

        cmd += "\n WHERE week = {};".format(date)
        self.cursor.execute(cmd)


    def _create_player_stats_table(self, player):
        """
        called by _add_player() to initialize the table named for the player,
        consisting of all of their stats keyed by week
        """
        try:
            self.cursor.execute("SELECT * FROM {};".format(player))
        except MySQLdb.Error:
            cmd = "CREATE TABLE " + player + "("
            fields = stats_headers.PLAYER_STATS.items()
            for (name, value) in fields:
                cmd += name + " " + value + ", \n"
            cmd += "PRIMARY KEY (week));"
            self.cursor.execute(cmd)
            self._db.commit()


    def _create_teams_table(self):
        """create the global teams table"""
        try:
            self.cursor.execute("SELECT * FROM teams;")
        except MySQLdb.Error:
            self.cursor.execute("CREATE TABLE teams(name TEXT);")
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

