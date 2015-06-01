"""
tkinter windows for displaying stats from statsdb.StatsDBOutput
"""
import Tkinter as tk
import statsdb

#tk.Frame gives us a ton of public methods.
#Also, I think usage of single letter variable names is perfectly fine,
# so long as it's clear. so:
#pylint: disable=too-many-public-methods
#pylint: disable=invalid-name


class OutputWindow(tk.Frame):

    """ Window for general output interface
    """

    def __init__(self, master=None):
        self.select_team = self.teams_menu = None
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
        self._create_quit_button()
        self._create_teams_menu()
        self._create_year_menu()
        self._create_show_roster_button()


    def _create_quit_button(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit,
                                       width=6)
        self.quit_button.grid(row=5, column=2, padx=10, pady=10)


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

        years = self.stats.get_years()

        for y in years:
            self.year_menu.insert(tk.END, y)
        self.year_menu.grid(row=2, column=2, padx=10, pady=10)


    def _create_show_roster_button(self):
        self.show_roster_button = tk.Button(self, text='Get Roster',
                                            command=self._show_roster)
        self.show_roster_button.grid(row=5, column=1, padx=10, pady=10)


    def _show_roster(self):
        """
        show the roster for the selected team and year in a separate pop-up
        """
        team = self.teams_menu.get(tk.ACTIVE)
        year = self.year_menu.get(tk.ACTIVE)
        players = self.stats.get_players(team, year)
        RosterWindow(players, team, year)


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
        self._create_quit_button()


    def _create_window(self, team, year):
        self.grid(ipadx=5, ipady=5)
        if team and year:
            self.master.title('Roster for ' + team + ', ' + year)

    def _display_roster(self, players):
        self.roster = tk.Listbox(self)
        for p in players:
            self.roster.insert(tk.END, p)
        self.roster.grid(row=1, column=1)

    def _create_quit_button(self):
        self.quit_button = tk.Button(self, text='Quit',
                                     command=self.master.destroy)
        self.quit_button.grid(row=2)


if __name__ == '__main__':
    APP = OutputWindow()
    APP.mainloop()

