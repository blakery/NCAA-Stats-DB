import Tkinter as tk



class OutputWindow(tk.Frame):
    """ Window for output interface
    """

    def __init__(self):

        self.parent = tk.Toplevel()
        tk.Frame.__init__(self, self.parent)
        self._populate_objects()
        self._create_window()


    def _populate_objects(self):
        pass

    def _create_window(self):
        """create the main window"""
        self.parent.title('View Database Statistics')
        self.grid(ipadx=5, ipady=5)


