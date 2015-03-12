import Tkinter as tk
import Config


class SettingsWindow(tk.Frame):

    
    def __init__(self):
        self.parent = tk.Toplevel()
        tk.Frame.__init__(self, self.parent)
        self.grid()         
        self.populateObjects()

            
    def populateObjects(self):
        self.createSetUserNameOption()
        self.createSetDBOption()
        
    def createSetUserNameOption(self):
        self.userNameButton = tk.Button(self, command=self.setUserNameSubmit,
            text="Set SQL User Name", width=22, anchor=tk.W, justify=tk.LEFT)
        self.userNameButton.grid(row=1, column=0)
        self.userNameEntry = tk.Entry(self, exportselection=0)
        self.userNameEntry.grid(row=1, column=1)
        self.userNameEntry.insert(0, Config.getSQLUserName())
        
    def createSetDBOption(self):
        self.dBButton = tk.Button(self, command=self.setDBSubmit,
            text="Set SQL Database", width=22, anchor=tk.W, justify=tk.LEFT)
        self.dBButton.grid(row=2, column=0)
        
        self.dBEntry = tk.Entry(self, exportselection=0)
        self.dBEntry.grid(row=2, column=1)       
        self.dBEntry.insert(0, Config.getSQLDB())       
       

    def setUserNameSubmit(self):
        text = self.userNameEntry.get() #FIXME: Security concern: need to think about further validating user input
        if text == Config.getSQLUserName(): pass
        else: Config.setSQLUserName(text)
        
        
    def setDBSubmit(self):
        text = self.dBEntry.get()  #FIXME: Security concern: need to think about further validating user input
        if text == Config.getSQLDB(): pass
        else: Config.setSQLDB(text)
        
        
        
