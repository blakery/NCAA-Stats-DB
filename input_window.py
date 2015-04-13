"""Interface for inputting stat files"""
import Tkinter as tk
import ProcessStats


class InputWindow(tk.Frame):
#tk.Frame gives us a ton of public methods. so:
#pylint: disable=too-many-public-methods

    """Window for the interface for inputting stat files"""

    def __init__(self):
        #Attributes:
        self.cancel_button = None
        self.settings_button = None
        self.entry_variable = None
        self.text_entry = None
        self.settings = None
        self.submit_button = None

        self.parent = tk.Toplevel()
        tk.Frame.__init__(self, self.parent)
        self._populate_objects()
        self._create_window()

    def _create_window(self):
        """create the main window"""
        self.parent.title('Input Stat Files')
        self.grid(ipadx=5, ipady=5)


    def _populate_objects(self):
        """fill in the window"""
        self._create_text_entry()
        self._create_submit_button()
        self._create_cancel_button()


    def _create_submit_button(self):
        """self-explanitorys"""
        self.submit_button = tk.Button(self, text='Submit',
                                      command=self._submit_file)
        self.submit_button.grid(row=0, column=1)

    def _create_cancel_button(self):
        """self-explanitory"""
        self.cancel_button = tk.Button(self, text='Cancel',
                                       command=self.parent.destroy)
        self.cancel_button.grid(row=0, column=2)


    def _create_text_entry(self):
        """self explanitory"""
        self.entry_variable = tk.StringVar()
        self.entry_variable.set('Enter a filename or directory')
        self.text_entry = tk.Entry(self, exportselection=0, width=30,
                                textvariable=self.entry_variable)
        self.text_entry.grid(row=0, column=0, padx=10, pady=10)

    def _submit_file(self):
        """called when the submit button is pressed - process the file"""
        text = self.entry_variable.get()
        if(text == 'Enter a filename or directory') | (text == ''):
            pass
        else:
            ProcessStats.process(text)
            self.entry_variable.set('Enter a filename or directory')



if __name__ == '__main__':
    APP = InputWindow()
    APP.mainloop()


