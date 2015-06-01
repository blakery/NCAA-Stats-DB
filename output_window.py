import Tkinter as tk
import statsdb


class OutputWindow(tk.Frame):
    #tk.Frame gives us a ton of public methods. so:
    #pylint: disable=too-many-public-methods
    """ Window for output interface
    """

    def __init__(self, master=None):
        self.quit_button = self.select_team = self.teams_menu = None

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

    def _create_quit_button(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit,
                                       width=6)
        self.quit_button.grid(row=5, column=2, padx=10, pady=10)


    def _create_teams_menu(self):
        self.select_team = tk.Label(self, text='Select a Team')
        self.select_team.grid(row=2, column=1)
        
        self.teams_menu = tk.Listbox(self)
        
        teams = self.stats.get_teams()        
        for i in teams:
            self.teams_menu.insert(tk.END, i)
        self.teams_menu.grid(row=3, column=1, padx=10, pady=10)

    def _get_selected_team(self):
        return self.teams_menu.get(tk.ACTIVE)


if __name__ == '__main__':
    APP = OutputWindow()
    APP.mainloop()
