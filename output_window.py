import Tkinter as tk
import statsdb


class OutputWindow(tk.Frame):
    """ Window for output interface
    """
#tk.Frame gives us a ton of public methods. so:
#pylint: disable=too-many-public-methods
    def __init__(self, master=None):
        self.quit_button = None
        self.teams_menu = None
        self.select_team = None

        tk.Frame.__init__(self, master)
#        self.pack()
        self.stats = statsdb.StatsDBOutput()


        self._create_window()
        self._populate_objects()



    def _create_window(self):
        """create the output window"""
        self.grid(ipadx=5, ipady=5)
        self.master.title('View Database Statistics')


    def _populate_objects(self):
        self.quit_button = self._create_quit_button()
        self.teams_menu = self._create_teams_menu()

    def _create_quit_button(self):
        """self-explanitory"""
        self.quit_button = tk.Button(self, text='Quit', command=self.quit,
                                       width=6)
        self.quit_button.grid(row=2, column=1, padx=10, pady=10)


    def _create_teams_menu(self):
        """
        self.select_team = tk.Menubutton(self, text="Select Team")
        self.select_team.grid(row=2, padx=10, pady=10)
        
        self.teams_menu = tk.Menu(self.select_team, tearoff=0)
        
        self.teams_menu.add_checkbutton(self,label="foo", variable=tk.IntVar())
        self.teams_menu.add_checkbutton(self,label="bar", variable=tk.IntVar())

        self.select_team['menu'] = self.teams_menu
        """
        self.select_team = tk.Listbox(self)
        teams = self.stats.get_teams()
        for i in teams:
            self.select_team.insert(tk.END, i)
        self.select_team.grid(row=1, padx=10, pady=10)


if __name__ == '__main__':
    APP = OutputWindow()
    APP.mainloop()
