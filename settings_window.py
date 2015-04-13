"""Module contains:
    SettingsWindow, Interface to change settings.
"""
import Tkinter as tk
import Config


class SettingsWindow(tk.Frame):
#tk.Frame gives us a ton of public methods. so:
#pylint: disable=too-many-public-methods, too-many-instance-attributes
    """ Interface to change settings.
        Users can change:
        mysql username, database, and host
    """

    def __init__(self):
        self.user_name_button = None
        self.db_button = None
        self.db_entry = None
        self.set_host_button = None
        self.user_name_entry = None
        self.host_entry = None
        self.cancel_button = None

        self.parent = tk.Toplevel()
        tk.Frame.__init__(self, self.parent)
        self._populate_objects()
        self.grid()


    def _populate_objects(self):
        """create all of the objects for the window"""
        self._create_set_user_name_option()
        self._create_set_db_option()
        self._create_set_host_option()
        self._create_cancel_button()

    def _create_set_user_name_option(self):
        """create the field and button to set the user name """
        self.user_name_button = tk.Button(self,
            command=self._set_user_name_submit,
            text="Set SQL User Name", width=22, anchor=tk.W, justify=tk.LEFT)
        self.user_name_button.grid(row=1, column=0)
        self.user_name_entry = tk.Entry(self, exportselection=0)
        self.user_name_entry.grid(row=1, column=1)
        self.user_name_entry.insert(0, Config.getSQLUserName())

    def _create_set_db_option(self):
        """create the field and button to set the database"""
        self.db_button = tk.Button(self, command=self._set_db_submit,
            text="Set SQL Database", width=22, anchor=tk.W, justify=tk.LEFT)
        self.db_button.grid(row=2, column=0)

        self.db_entry = tk.Entry(self, exportselection=0)
        self.db_entry.grid(row=2, column=1)
        self.db_entry.insert(0, Config.getSQLDB())


    def _create_set_host_option(self):
        """create the field and button to set the host"""
        self.set_host_button = tk.Button(self, command=self._set_host_submit,
            text="Set SQL Host", width=22, anchor=tk.W, justify=tk.LEFT)
        self.set_host_button.grid(row=3, column=0)

        self.host_entry = tk.Entry(self, exportselection=0)
        self.host_entry.grid(row=3, column=1)
        self.host_entry.insert(0, Config.getSQLHost())

    def _create_cancel_button(self):
        """self-explanatory"""
        self.cancel_button = tk.Button(self, command=self.parent.destroy,
            text="Cancel", anchor=tk.W, justify=tk.LEFT)
        self.cancel_button.grid(row=4, column=0)

    def _set_user_name_submit(self):
        """ called when someone clicks the button to submit a change
            to the user name
        """
        text = self.user_name_entry.get()
        if text == Config.getSQLUserName():
            pass
        else:
            Config.setSQLUserName(text)


    def _set_db_submit(self):
        """ called when someone clicks the button to submit a change
            to the database
        """
        text = self.db_entry.get()
        if text == Config.getSQLDB():
            pass
        else:
            Config.setSQLDB(text)


    def _set_host_submit(self):
        """ called when someone clicks the button to submit a change
            to the host
        """
        text = self.host_entry.get()
        if text == Config.getSQLHost():
            pass
        else:
            Config.setSQLHost(text)

