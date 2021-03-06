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
import stats_processing_errors as errors




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
    if not names_ret or not stats_ret:
        return edit_stats(stats[1:], names[1:], [name], [val])
    else:
        names_ret.append(name)
        stats_ret.append(val)
        return edit_stats(stats[1:], names[1:], names_ret, stats_ret)


class StatsDBInput(object):
    """
    Class for adding entries to the stats database in the form
    given by the parser

    """
    def __init__(self, host=None, user=None, password="", db=None):
        self._db = self.cursor = None
        self.teams_added = self.teams_updated = 0
        self.players_added = self.players_updated = 0

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
                self.add_player_stats(player[1:], header[1:], date)
        else:
            for team in block[1:]:
                self.add_team_stats(team[1:], header[1:], date)
        try: 
            self.cursor.execute("COMMIT;")
        except MySQLdb.Error, args:
            errors.mysql_input_error(args, action="Committing changes")


    def add_team_stats(self, stats, headers, date):
        """
        Decides whether to add a new entry for a team, or update an existing
        entry, and calls the apropriate function.
        """
        cmd = "SELECT * FROM TeamStats WHERE Name = %s AND week = %s;"
        try: self.cursor.execute(cmd, [stats[0], date])
        except MySQLdb.Error, args:
            action = "Querying TeamStats for %s".format(stats[0])
            errors.mysql_input_error(args, stats=stats, headers=headers,
                                     date=date, action=action)
        if len(self.cursor.fetchall()):
            if self._update_team_stats(stats, headers, date):
                self.teams_updated += 1
        else:
            if self._add_new_team_stats(stats, headers, date):
                self.teams_added += 1


    def _update_team_stats(self, stats, headers, date):
        """
        update team statistics to the TeamStats table
        stats is a list consisting of: [team name, stats...]
        """
        names, values = edit_stats(stats[1:], headers[1:])
        if not names or not values: 
            return False

        cmd = "UPDATE TeamStats SET {} = %s ".format(names[0])
        for i in range(1, min((len(names)), (len(values)))):
            cmd += ", " + names[i] + " = %s " 
        cmd += "WHERE name = %s AND Week = %s;"
        values.append(stats[0])
        values.append(date)

        try: self.cursor.execute(cmd, values)
        except MySQLdb.Error, args:
            action = "Updating a team"
            errors.mysql_input_error(args, stats=stats, headers=headers,
                                     date=date, action=action)
            return False
        else:
            return True


    def _add_new_team_stats(self, stats, headers, date):
        """
        add team statistics to the TeamStats table
        stats is a list consisting of: [team name, stats...]
        """
        self._add_team(stats[0])

        names, values = edit_stats(stats, headers)
        cmd = "INSERT INTO TeamStats("
        for n in names:
            cmd += n + ", "
        cmd += "week) VALUES("
        for _ in values:
            cmd += "%s, "
        cmd += "%s);"
        values.append(date)

        try:
            self.cursor.execute(cmd, values)
        except MySQLdb.Error, args:
            action = "Adding a new TeamStats entry"
            errors.mysql_input_error(args, stats=stats, headers=headers,
                                     date=date, action=action)
            return False
        else: return True


    def _add_team(self, school):
        """
        add appropiate entries and tables to the database for a new team:
            - creates a team roster table
            - adds the team to the teams table
        """
        self._create_table_for_team(school)
        try:
            self.cursor.execute("SELECT * FROM teams WHERE name = %s;", school)
        except MySQLdb.Error, args:
            action = 'Querying teams for "%s"'.format(school)
            errors.mysql_input_error(args, action=action)

        if len(self.cursor.fetchall()) == 0:
            try:
                cmd = "INSERT INTO teams(name) VALUES(%s);"
                self.cursor.execute(cmd, school)
            except MySQLdb.Error, args:
                action = 'Inserting "%s" into teams table'.format(school)
                errors.mysql_input_error(args, action=action)


    def _create_table_for_team(self, school):
        """
        create a table for 'school', if needed, for it's players' stats
        """
        fields = stats_headers.PLAYER_STATS.items()
        name, value = fields[0]
        cmd = "CREATE TABLE IF NOT EXISTS {} (\n{} {}".format(
            school, name, value)
        for (name, value) in fields[1:]:
            cmd += ",\n{} {}".format(name, value)
        cmd += "\n);"

        try:
            self.cursor.execute("SET sql_notes = 0; ") 
            self.cursor.execute(cmd)
        except MySQLdb.Error, args:
            action = "Creating table for {}".format(school)
            errors.mysql_input_error(args, action=action)
        finally:
            self.cursor.execute("SET sql_notes = 1; ") 


    def add_player_stats(self, stats, headers, date):
        """
        Add player stats to the sql database
        stats is a list in the form of [name, school, stats...]
        headers is a list of the corresponding column names
        """
        self._add_team(stats[1])
        cmd = "SELECT * FROM {} WHERE Name = %s AND Week = %s;".format(stats[1])
        
        try: self.cursor.execute(cmd, [stats[0], date])
        except MySQLdb.Error, args:
            action = "Querying %s for player".format(stats[1])
            errors.mysql_input_error(args, stats=stats, headers=headers,
                                     date=date, action=action)
        if len(self.cursor.fetchall()) == 0:
            if self._add_new_player_stats(stats, headers, date):
                self.players_added += 1
        else:
            if self._update_player_stats(stats, headers, date):
                self.players_updated += 1



    def _add_new_player_stats(self, stats, headers, date):
        """called by add_player_stats() to add a new player """

        revised_headers, values = edit_stats(stats[2:], headers[2:])

        cmd = "INSERT INTO " + stats[1] + "(name, Week"

        if revised_headers and values:
            for h in revised_headers:
                cmd += ", " + h
            cmd += ") VALUES(%s , %s"
            for _ in values:
                cmd += ", %s "
            cmd += ");"
            values.insert(0, date)
            values.insert(0, stats[0])
        else:
            cmd += ") VALUES(%s , %s);"
            values = [stats[0], date]
        try:
            self.cursor.execute(cmd, values)
        except MySQLdb.Error, args:
            action = "Adding a new player stats entry to %s".format(stats[1])
            errors.mysql_input_error(args, stats=stats, headers=headers,
                                     date=date, action=action)
            return False
        else: return True



    def _update_player_stats(self, stats, headers, date):
        """called by add_player_stats() to update an existing player"""

        revised_headers, values = edit_stats(stats[2:], headers[2:])
        if not revised_headers or not values:
            return False   # can't update if we don't have any stats

        cmd = "UPDATE " + stats[1] + "\nSET " + revised_headers[0] + " = %s "
        for n in revised_headers[1:]:
            cmd += ", " + n + " = %s"
        cmd += " WHERE (name = %s ) AND (week = %s );"
        values.append(stats[0])
        values.append(date)
        try:
            self.cursor.execute(cmd, values)
        except MySQLdb.Error, args:
            errors.mysql_input_error(args, stats, headers, date)
            return False
        else: return True


    def _create_teams_table(self):
        """create the global teams table"""
        try:
            self.cursor.execute("SET sql_notes = 0; ") 
            self.cursor.execute("CREATE TABLE IF NOT EXISTS teams(name TEXT);")
        except MySQLdb.Error, args:
            errors.mysql_input_error(args, action="Creating teams table")
        finally:
            self.cursor.execute("SET sql_notes = 1; ") 

    def _create_team_stats_table(self):
        """create the global teamstats table"""
        cmd = "CREATE TABLE IF NOT EXISTS TeamStats("
        fields = stats_headers.TEAM_STATS.items()
        cmd += fields[0][0] + " " + fields[0][1]
        for (name, value) in fields[1:]:
            cmd += ", " + name + " " + value
        cmd += ");"
        try: 
            self.cursor.execute("SET sql_notes = 0; ") 
            self.cursor.execute(cmd)
        except MySQLdb.Error, args:
            action = "Creating TeamStats table"
            errors.mysql_input_error(args, action=action)
        finally:
            self.cursor.execute("SET sql_notes = 1; ") 



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
        returns the roster of a team for a particular year as a list.
        If year is None, returns all players for the team.
        '''
        if year:
            cmd = "SELECT * FROM " + team + " WHERE YEAR(Week) = %s;"
            self.cursor.execute(cmd, year)
        else:
            cmd = "SELECT * FROM " + team + ";"
            self.cursor.execute(cmd)
        players = []
        player_data = self.cursor.fetchall()

        desc = self.cursor.description
        i = 0
        while i < len(desc) and desc[i][0] != 'Name':
            i += 1

        for p in player_data:
            players.append(p[i])
        return players


    def get_years(self):
        """Get a list of all the years for which statics exist in the db"""
        cmd = "SELECT DISTINCT(YEAR(Week)) FROM TeamStats ORDER BY week;"
        self.cursor.execute(cmd)
        years = []
        dates = self.cursor.fetchall()
        for each in dates:
            years.append(each[0])
        return years


    def get_team_stats(self, team):
        '''
        returns a tuple of a list containing the column descriptions and a list
        of each line of stats for the team indicated. so: ([], [[]])
        '''
        cmd = "SELECT * FROM TeamStats WHERE Name = %s;"
        self.cursor.execute(cmd, team)

        team_stats_tuples = self.cursor.fetchall()
        team_stats = []
        for line in team_stats_tuples:
            line = team_stats.append(list(line))
            
        desc = self.cursor.description
        column_names = []
        for d in desc:
            column_names.append(d[0])

        return column_names, team_stats

