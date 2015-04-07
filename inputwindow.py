"""ui for inputting csv stat files"""
import Tkinter as tk
import ProcessStats
import SettingsWindow


class InputWindow(tk.Frame):
    """ui for inputting csv stat files"""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #Attributes:
        self.cancel_button = None
        self.settings_button = None
        self.entry_variable = None
        self.text_entry = None
        self.settings = None
        self.submit_button = None
        self._create_window(master)
        self._populate_objects()


    def _create_window(self, master):
        """create the main window"""
        self.grid(ipadx=5, ipady=5)
        self.master.title('Process Stat Files')

    def _populate_objects(self):
        """fill in the window"""
        self._create_text_entry()
        self._create_submit_button()
        self._create_cancel_button()
        self._create_settings_button()

    def _create_submit_button(self):
        """obvious"""
        self.submit_button = tk.Button(self, text='Submit',
                                      command=self.submit_file)
        self.submit_button.grid(row=0, column=1)

    def _create_cancel_button(self):
        """obvious"""
        self.cancel_button = tk.Button(self, text='Cancel', command=self.quit)
        self.cancel_button.grid(row=0, column=2)

    def _create_settings_button(self):
        """obvious"""
        self.settings_button = tk.Button(self, text='Settings',
                                      command=self.show_settings)
        self.settings_button.grid(row=1, column=1, padx=10, pady=10)

    def _create_text_entry(self):
        """obvious"""
        self.entry_variable = tk.StringVar()
        self.entry_variable.set('Enter a filename or directory')
        self.text_entry = tk.Entry(self, exportselection=0, width=30,
                                textvariable=self.entry_variable)
        self.text_entry.grid(row=0, column=0, padx=10, pady=10)

    def submit_file(self):
        """called when the submit button is pressed - process the file"""
        text = self.entry_variable.get()
        if(text == 'Enter a filename or directory') | (text == ''):
            pass
        else:
            ProcessStats.process(text)
            self.entry_variable.set('Enter a filename or directory')

    def show_settings(self):
        """bring up the settings window"""
        self.settings = SettingsWindow.SettingsWindow()


if __name__ == '__main__':
    app = InputWindow()
    app.mainloop()


