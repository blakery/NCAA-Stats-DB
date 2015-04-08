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


def translate_player_stats(stats, index, name):
    """
    called return the sql name and data type of the name as it's
    listed in the ncaa stats files
    """
    if name == 'Ht':
        return (name, stats[index] + "." + stats.pop(index + 1))
    elif name == 'TO':
        return ('TURNOVERS', stats[index])
    elif stats_headers.PLAYER_STATS[name] == 'TEXT':
        return (name, "'{}'".format(stats[index]))
    else: return (name, stats[index])




class StatsDB(object):
    """
    Class for adding entries to the stats database in the form
    given by the parser

    Attributes:
        _db -- database connection returned by MySQLdb.connect()
        cursor -- cursor object returned by _db.connect()
    """
#DatabaseError

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
        except OperationalError, args:
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
        # team stats do not
        # exclude the first column, the numerical ranking, as it's
        #   a. a derived statistic, and
        #   b. too variable and inconsitant to be of any use.
        # date = "'" + date + "'"
        if len(header) < 3:
            print "invalid header: " + str(header)
        elif header[2] == 'Team':
            for player in block[1:]:
                self._add_player_stats(player[1:], header[1:], date)
        else:
            for team in block[1:]:
                self._add_team_stats(team[1:], header[1:], date)


    def _add_team_stats(self, stats, headers, date):
        """
        add team statistics to the TeamStats table
        stats is a list consisting of: [team name, stats...]
        """
        self._add_team(stats[0])
        columns = "week"
        values = date

        for i in range(len(headers)):
            if headers[i] == 'TO':
                headers[i] = 'TURNOVERS'
            columns += ", " + headers[i]
            if stats_headers.TEAM_STATS[headers[i]] == 'TEXT':
                values += ", '{}'".format(stats[i])
            else:
                values += ", " + stats[i]
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



    def _add_player_stats(self, stats, headers, date):
        """
        Add player stats to the sql database
        stats is a list in the form of [name, school, stats...]
        headers is a list of the corresponding column names
        """
        self._add_player(stats[0], stats[1])

        self.cursor.execute(
            "SELECT * FROM {} WHERE week = {};".format(stats[0], date))
        if len(self.cursor.fetchall()) == 0:
            self._add_new_player_stats(stats, headers, date)
        else:
            self._update_player_stats(stats, headers, date)


    def _add_player(self, player, school):
        """
        called by add_player_stats() each time it executes
        checks to see if the player named is already listed.
        if not, adds the player to the school's roster and creates a table
        for the player's stats.
        """
        self._add_team(school)
        self.cursor.execute(
            "SELECT * FROM {} WHERE player = '{}';".format(school, player))
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute(
                "INSERT INTO {}(player) VALUES('{}');".
                format(school, player))
            self._create_player_stats_table(player)
            self._db.commit()
        else: pass


    def _add_new_player_stats(self, stats, headers, date):
        """called by add_player_stats() to add a new player """
        columns = "week"
        values = date

        for i in range(2, len(headers) -1):
            field, val = translate_player_stats(stats, i, headers[i])
            columns += ", " + field
            values += ", " + val
        cmd = "INSERT INTO {}({}) VALUES ({})".format(stats[0], columns, values)
        self.cursor.execute(cmd)


    def _update_player_stats(self, stats, headers, date):
        """called by add_player_stats() to update an existing player"""
        cmd = "UPDATE {} \n".format(stats[0])
        field, val = translate_player_stats(stats, 2, headers[2])
        cmd += "SET {} = {}".format(field, val)

        for i in range(2, len(stats) -1):
            (field, val) = translate_player_stats(stats, i, headers[i])
            cmd += ", {} = {}".format(field, val)

        cmd += "\n WHERE week = {};".format(date)
        self.cursor.execute(cmd)


    def _create_player_stats_table(self, player):
        """
        called by _addPlayer() to initialize the table named for the player,
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


    def execute(self, cmd):
        """
        a wrapper for cursor.execute(), used primarily for tests.
        this may go away at some point
        """
        self.cursor.execute(cmd)
