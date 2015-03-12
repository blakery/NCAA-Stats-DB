import Tkinter as tk
import ProcessStats
import SettingsWindow


class InputWindow(tk.Frame):

    def __init__(self, master=None):
        self.createWindow(master)
        self.populateObjects()



    def createWindow(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        #self.mainFrame=tk.Frame()
        #self.mainFrame.grid()
        self.master.title('Process Stat Files')

    def populateObjects(self):
        self.createTextEntry()
        self.createSubmitButton()
        self.createCancelButton()
        self.createSettingsButton()

    def createSubmitButton(self):
        self.submitButton = tk.Button(self, text='Submit', command=self.submitFile)
        self.submitButton.grid(row=0, column=1)


    def createCancelButton(self):
        self.cancelButton=tk.Button(self, text='Cancel', command=self.quit)
        self.cancelButton.grid(row=1, column=1)

    def createSettingsButton(self):
        self.settingsButton=tk.Button(self, text='Settings', command=self.showSettings)
        self.settingsButton.grid(row=1, column=2)


    def createTextEntry(self):
        self.textEntry=tk.Entry(self, exportselection=0, width=30)
        self.textEntry.grid(row=0, column=0)
        self.textEntry.insert(0,'Enter a filename or directory')



    def submitFile(self):
        f = self.textEntry.get()
        # don't take any action for no entry
        if(f == 'Enter a filename or directory') | (f==''): pass
        else: ProcessStats.main([None, f])

        
    def showSettings(self):
        self.settings=SettingsWindow.SettingsWindow()
        self.mainloop()
        
if __name__ == '__main__':
    app = InputWindow()
    app.mainloop()


