"""
    statsdb - contains StatsDB, a class for adding lists of stats to the
    mysql database

    TO CONSIDER: switch to using MySQL Connector/Python. Advantages:
        works with python 2 and 3.
        appears to be better maintained and the more cannonical choice at this
            point

    TO CONSIDER: numerical keys and foreign keys

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





def edit_stats(stats, names, names_ret=None, stats_ret=None):
    ''' 
    return a properly formatted list of stats and their
    corresponding names, derived from stats and names.
    Removes None values, empty strings, and stats that are ignored.
    If the stat is height ("Ht"), [h1, h2] (originally h1 - h2, 
        representing h1' h2 ") becomes h1.(h2 / 12).
    '''
    def get_edited_name(names):
        if type(names) != list:
            return None 
        elif not names[0] or names[0] == '' or \
        names[0] in stats_headers.IGNORE_STATS:
            return None
        elif names[0] == 'TO':
            return 'TURNOVERS'
        else: return names[0]

    def get_edited_val(stats, name):
        if type(stats) != list:
            return None
        elif not stats[0] or stats[0] == '':
            return None
        elif name == 'Ht':
            return stats.pop(0) + "." + str(int(stats[0]) / 12)
        else:
            return stats[0]

    if not names or not stats: # base case: empty lists
        return (names_ret, stats_ret)
        
    name = get_edited_name(names)
    if not name:
        return edit_stats(stats[1:], names[1:], names_ret, stats_ret)

    val = get_edited_val(stats, name)
    if not val: 
        return edit_stats(stats[1:], names[1:], names_ret, stats_ret)
    
    if not names_ret or not stats_ret or \
    type(names_ret) != list or type(stats_ret) != list:
        return edit_stats(stats[1:], names[1:], [name], [val])
    else:
        names_ret.append(name)
        stats_ret.append(val)
        return edit_stats(stats[1:], names[1:], names_ret, stats_ret)


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
                    print args
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

        names, values = edit_stats(stats[1:], headers[1:])

        cmd = "INSERT INTO TeamStats("
        for n in names:
            cmd += n + ", "
        cmd += "week) VALUES("
        for _ in values:
            cmd += "%s, "
        cmd += "%s);"

        values.append(date)

        self.cursor.execute(cmd, values)


    def _add_team(self, school):
        """
        add appropiate entries and tables to the database for a new team:
            - creates a team roster table
            - adds the team to the teams table
        """
        self.cursor.execute("SELECT * FROM teams WHERE name = %s;", school)
        
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute("INSERT INTO teams(name) VALUES(%s);", school)

        try: 
            self.cursor.execute("SELECT * FROM {};".format(school))
        except MySQLdb.Error:
            fields = stats_headers.PLAYER_STATS.items()
            name, value = fields[0]
            field_names = name + " " + value
            for (name, value) in fields[1:]:
                field_names += ", \n" + name + " " + value
            self.cursor.execute(
                "CREATE TABLE {} ({});".format(school, field_names))
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

        cmd = "SELECT * FROM " + team + " WHERE Name = %s AND Week = %s;"
        self.cursor.execute(cmd, (name, date))

        if len(self.cursor.fetchall()) == 0:
            self._add_new_player_stats(stats, headers, date)
        else:
            self._update_player_stats(stats, headers, date)



    def _add_new_player_stats(self, stats, headers, date):
        """called by add_player_stats() to add a new player """

        revised_headers, values = edit_stats(stats[2:], headers[2:])

        cmd = "INSERT INTO " + stats[1] + "(name, Week"
        for h in revised_headers:
            cmd += ", " + h
        cmd += ") VALUES(%s , %s"
        for _ in values:
            cmd += ", %s "
        cmd += ");"
        
        values.insert(0, date)
        values.insert(0, stats[0])

        try:
            self.cursor.execute(cmd, values)
        except MySQLdb.Error, args:
            print args


    def _update_player_stats(self, stats, headers, date):
        """called by add_player_stats() to update an existing player"""

        revised_headers, values = edit_stats(stats[2:], headers[2:])

        cmd = "UPDATE " + stats[1] + "\nSET " + revised_headers[0] + " = %s "

        for n in revised_headers[1:]:
            cmd += ", " + n + " = %s"

        cmd += " WHERE (name = %s ) AND (week = %s );"
        values.append(stats[0])
        values.append(date)
        try:
            self.cursor.execute(cmd, values)
        except Exception, args:
            print args
            print cmd

    def _create_teams_table(self):
        """create the global teams table"""
        #FIXME: check if resource exists in a more sensible way (ie IF EXISTS)
        try:
            self.cursor.execute("SELECT * FROM teams;")
        except MySQLdb.Error:
            self.cursor.execute("CREATE TABLE teams(name TEXT);")
        self.cursor.execute("COMMIT;")


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
    Output values from the db
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
        self.cursor.execute("SELECT * FROM teams;")
        teams = []
        for t in self.cursor.fetchall():
            teams.append(t[0])
        return teams


    def get_players(self, team, year):
        '''
        returns the roster of a team for a particular year as a list
        '''

        cmd = "SELECT * FROM " + team + " WHERE YEAR(Week) = %s;"
        self.cursor.execute(cmd, year)
        players = []
        player_data = self.cursor.fetchall()

        desc = self.cursor.description
        i = 0
        while i < len(desc) and desc[i][0] != 'Name':
            i += 1

        for p in player_data:
            players.append(p[i])
        return players



