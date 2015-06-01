import Tkinter as tk
import statsdb


class OutputWindow(tk.Frame):
    #tk.Frame gives us a ton of public methods. so:
    #pylint: disable=too-many-public-methods
    """ Window for output interface
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
        self._create_quit_button()
        self._create_teams_menu()
        self._create_year_menu()
        self._create_show_roster_button()

    def _create_quit_button(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit,
                                       width=6)
        self.quit_button.grid(row=5, column=2, padx=10, pady=10)


    def _create_teams_menu(self):
        self.select_team = tk.Label(self, text='Select a Team')
        self.select_team.grid(row=1, column=1)
        
        self.teams_menu = tk.Listbox(self, exportselection=False)
        
        teams = self.stats.get_teams()        
        for i in teams:
            self.teams_menu.insert(tk.END, i)
        self.teams_menu.grid(row=2, column=1, padx=10, pady=10)



    def _create_year_menu(self):
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
        team = self.teams_menu.get(tk.ACTIVE)
        year = self.year_menu.get(tk.ACTIVE)
        players = self.stats.get_players(team, year)
        RosterWindow(players, team, year)


class RosterWindow(tk.Frame):

    def __init__(self, players, team=None, year=None):
        self.roster = self.quit_button = None
        
        self.parent = tk.Toplevel()
        tk.Frame.__init__(self, self.parent)

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
                                     command=self.parent.destroy)
        self.quit_button.grid(row=2)


if __name__ == '__main__':
    APP = OutputWindow()
    APP.mainloop()
