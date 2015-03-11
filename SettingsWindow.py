import Tkiter as tk
import Config


class SettingsUI.py(tk.Frame):

    def __init__(self, master):
        self.createWindow(master)
        
   
    def createWindow(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title('Settings')        
        
    

