"""
main window for the ui. right now, it just calls inputwindow
"""
import Tkinter as tk
import input_window
import settings_window


class MainWindow(tk.Frame):
    """The main window
    to implement:
        output button => output window
    """

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.settings_button = None
        self.settings = None
        self.input_window = None
        self.input_window_button = None
        self.quit_button = None
        self._create_window(master)
        self._populate()

    def _create_window(self, master):
        """create the main window"""
        self.grid(ipadx=5, ipady=5)
        self.master.title('Process Stat Files')

    def _populate(self):
        """populate the main window with it's elements"""
        self._create_settings_button()
        self._create_input_window_button()
        self._create_quit_button()

    def _create_quit_button(self):
        """self-explanitory"""
        self.cancel_button = tk.Button(self, text='Quit', command=self.quit,
                                       width=6)
        self.cancel_button.grid(row=2, column=2, padx=10, pady=10)

    def _create_input_window_button(self):
        """self-explanitory"""
        self.input_window_button = tk.Button(self, text='Input',
                                      command=self.open_input_window)
        self.input_window_button.grid(row=1, column=1, padx=10, pady=10)

    def _create_settings_button(self):
        """self-explanitory"""
        self.settings_button = tk.Button(self, text='Settings',
                                      command=self.show_settings)
        self.settings_button.grid(row=1, column=2, padx=10, pady=10)


    def open_input_window(self):
        """open an InputWindow"""
        self.input_window = input_window.InputWindow()

    def show_settings(self):
        """bring up the settings window"""
        self.settings = settings_window.SettingsWindow()

if __name__ == '__main__':
    App = MainWindow()
    App.mainloop()
