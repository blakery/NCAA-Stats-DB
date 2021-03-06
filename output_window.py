"""
tkinter windows for displaying stats from statsdb.StatsDBOutput
"""
import Tkinter as tk
import statsdb

#tk.Frame gives us a ton of public methods. Also, I think usage of single letter 
#variable names is perfectly fine, so long as the code is clear. so:
#pylint: disable=too-many-public-methods
#pylint: disable=invalid-name


class OutputWindow(tk.Frame):
    """
    Window for general output interface
    """

    def __init__(self, master=None):
        self.select_team = self.teams_menu = display_team_button = None
        self.select_year = self.year_menu = None
        self.show_roster_button = self.quit_button = None

        tk.Frame.__init__(self, master)
        self.stats = statsdb.StatsDBOutput()

        self._create_window()
        self._populate_objects()


    def _create_window(self):
        """create the output window"""
        self.grid(ipadx=5, ipady=5)
        self.master.title('View Database Statistics')


    def _populate_objects(self):
        """call methods to create all of the various objects"""
        self._create_teams_menu()
        self._create_year_menu()
        self._create_show_roster_button()
        self._create_display_team_button()
        self._create_quit_button()


    def _create_quit_button(self):
        """creates the button to quit the program """
        self.quit_button = tk.Button(self, text='Quit', command=self.quit,
                                       width=6)
        self.quit_button.grid(row=5, column=3, padx=10, pady=10)


    def _create_teams_menu(self):
        """create the listbox to select a team"""
        self.select_team = tk.Label(self, text='Select a Team')
        self.select_team.grid(row=1, column=1)

        self.teams_menu = tk.Listbox(self, exportselection=False)

        teams = self.stats.get_teams()
        for i in teams:
            self.teams_menu.insert(tk.END, i)
        self.teams_menu.grid(row=2, column=1, padx=10, pady=10)


    def _create_year_menu(self):
        """create the listbox to select a year"""
        self.select_year = tk.Label(self, text='Select a Year')
        self.select_year.grid(row=1, column=2)

        self.year_menu = tk.Listbox(self, exportselection=False)

        self.year_menu.insert(tk.END, "Select a year")
        years = self.stats.get_years()
        for y in years:
            self.year_menu.insert(tk.END, y)
        self.year_menu.grid(row=2, column=2, padx=10, pady=10)


    def _create_show_roster_button(self):
        """
        creates the button to display the roster of the selected team and year
        """
        self.show_roster_button = tk.Button(self, text='Get Roster',
                                            command=self._show_roster)
        self.show_roster_button.grid(row=5, column=1, padx=10, pady=10)


    def _show_roster(self):
        """
        show the roster for the selected team and year in a separate pop-up
        do nothing if a team and a year have not both been selected
        """
        team = self.teams_menu.get(tk.ACTIVE)
        year = self.year_menu.get(tk.ACTIVE)
        if year == "Select a year":
            players = self.stats.get_players(team, None)
            RosterWindow(players, team, None)
        elif team and year:
            players = self.stats.get_players(team, year)
            RosterWindow(players, team, year)


    def _create_display_team_button(self):
        """
        creates a button to show all stats for the selected team.
        """
        self.display_team_button = tk.Button(self, text="Display Team", 
                                             command=self._display_team)
        self.display_team_button.grid(row=5, column=2, padx=10, pady=10)


    def _display_team(self):
        """
        display the stats for the selected team
        """
        team = self.teams_menu.get(tk.ACTIVE)
        TeamStatsDisplay(team, self.stats)





class TeamStatsDisplay(tk.Frame):
    """
    A window that will display all of a team's stats
    """
    def __init__(self, team, db, master=None):
        self.stats_cols = self.quit_button = self.column_labels = self.team_stats_display = None

        if not master:
            self.master = tk.Toplevel()
        else:
            self.master = master
        tk.Frame.__init__(self, self.master)

        self._create_window(team)        
        
        columns, stats = db.get_team_stats(team)
        columns, stats = self._remove_empty_values(columns, stats)
        #self._create_column_labels(columns)
        #self._display_team_stats(stats)
        self._display_stats_in_separate_boxes(columns, stats)
        self._create_close_button()

    def _remove_empty_values(self, names, stats):
        """
        Takes a list of names and lines of stats, and removes all items if each
        stats entry is Null for that particular item.
        """
        names_ret = []
        stats_ret = []
        for i in range(1, len(stats)):
            stats_ret.append([])
        for i in range(0, len(names)-1):
            remove = True
            for line in stats:
                if (len(line) > i) and line[i] != None:
                    remove = False
            # Order properly as well as omiting empty columns:
            if remove is False:
                if names[i] == 'Name':
                    names_ret.insert(0, names[i])
                    for j in range(0, len(stats)-1):
                        stats_ret[j].insert(0, stats[j][i])    
                else:
                    names_ret.append(names[i])
                    for j in range(0, len(stats)-1):
                        stats_ret[j].append(str(stats[j][i]))

        return names_ret, stats_ret

    def _create_window(self, team):
        """Creates the window for the team's stats"""
        self.grid(ipadx=5, ipady=5)
        if team:
            self.master.title('Stats for ' + team)


    def _create_close_button(self):
        """Create a button to close the window"""
        self.quit_button = tk.Button(self, text='Close',
                                     command=self.master.destroy)
        self.quit_button.grid(row=2)

    def _display_stats_in_separate_boxes(self, names, stats):
        self.stats_cols = []
        for i in range(0, min(len(names), len(stats)) - 1):
            column = tk.Listbox(self)
            column.insert(tk.END, names[i])
            for line in stats:
                column.insert(tk.END, str(line[i]))
            column.grid(row=1, column=i+1)
            #column.grid()
            self.stats_cols.append(column)

    def _create_column_labels(self, columns):
        #TODO: Find a widget that formats this automatically
        labels = ''
        for label in columns:
            labels += label + " "
        self.column_labels = tk.Label(self, text=labels)
        self.column_labels.grid()


    def _display_team_stats(self, stats):
        self.team_stats_display = tk.Listbox(self)
        for line in stats:
            self.team_stats_display.insert(tk.END, str(line))
        self.team_stats_display.grid()


class RosterWindow(tk.Frame):
    """
    A window that will display the roster for a team in a particular year
    """
    def __init__(self, players, team, year, master=None):
        self.roster = self.quit_button = None
        if not master:
            self.master = tk.Toplevel()
        else:
            self.master = master
        tk.Frame.__init__(self, self.master)
        self._create_window(team, year)
        self._display_roster(players)
        self._create_close_button()


    def _create_window(self, team, year):
        """Creates the window for the roster"""
        self.grid(ipadx=5, ipady=5)
        if team and year:
            self.master.title('Roster for ' + team + ', ' + year)
        elif team:
            self.master.title('Roster for ' + team + ', all years')


    def _display_roster(self, players):
        """display the roster of players in a Listbox"""
        self.roster = tk.Listbox(self)
        for p in players:
            self.roster.insert(tk.END, p)
        self.roster.grid(row=1, column=1)


    def _create_close_button(self):
        """Create a button to close the window"""
        self.quit_button = tk.Button(self, text='Close',
                                     command=self.master.destroy)
        self.quit_button.grid(row=2)


if __name__ == '__main__':
    APP = OutputWindow()
    APP.mainloop()

