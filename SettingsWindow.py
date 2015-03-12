import Tkinter as tk
import Config


class SettingsWindow(tk.Toplevel):


    
    def __init__(self):
        tk.Toplevel.__init__(self)         
        self.populateObjects()

            
    def populateObjects(self):
        self.createSetUserNameButton()
        
    def createSetUserNameButton(self):
        self.userNameButton=tk.Button(self, text="Set SQL User Name")
        self.userNameButton.grid()
    
    def createSetDBButton(self):
        pass
       
