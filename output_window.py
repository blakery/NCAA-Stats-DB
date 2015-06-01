import Tkinter as tk
import statsdb


class OutputWindow(tk.Frame):
    """ Window for output interface
    """
#tk.Frame gives us a ton of public methods. so:
#pylint: disable=too-many-public-methods
    def __init__(self, master=None):

        tk.Frame.__init__(self, master)

        self.quit_button = None

        self._create_window()
        self._populate_objects()



    def _create_window(self):
        """create the output window"""
        self.grid(ipadx=5, ipady=5)
        self.master.title('View Database Statistics')


    def _populate_objects(self):
        self.quit_button = self._create_quit_button()


    def _create_quit_button(self):
        """self-explanitory"""
        self.quit_button = tk.Button(self, text='Quit', command=self.quit,
                                       width=6)
        self.quit_button.grid(row=1, column=1, padx=10, pady=10)

    


if __name__ == '__main__':
    APP = OutputWindow()
    APP.mainloop()
