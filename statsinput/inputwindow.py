import Tkinter as tk
import statsinput.ProcessStats
import SettingsWindow
import sys
import os

class InputWindow(tk.Frame):

    def __init__(self, master=None):
        self.createWindow(master)
        self.populateObjects()

    def createWindow(self, master):
        tk.Frame.__init__(self, master)
        self.grid(ipadx=5,ipady=5)
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
        self.cancelButton.grid(row=0, column=2)


    def createSettingsButton(self): #FIXME : change to menu option
        self.settingsButton=tk.Button(self, text='Settings', command=self.showSettings)
        self.settingsButton.grid(row=1, column=1, padx=10, pady=10)


    def createTextEntry(self):
        self.entryVariable = tk.StringVar()
        self.entryVariable.set('Enter a filename or directory')
        self.textEntry=tk.Entry(self, exportselection=0, width=30, 
            textvariable=self.entryVariable)

        self.textEntry.grid(row=0, column=0,padx=10, pady=10)



    def submitFile(self):
        f = self.entryVariable.get()
        # don't take any action for no entry
        if(f == 'Enter a filename or directory') | (f==''): pass
        else: 
            ProcessStats.process(f)
            self.entryVariable.set('Enter a filename or directory')
        
    def showSettings(self):
        self.settings=SettingsWindow.SettingsWindow()


        
if __name__ == '__main__':
    app = InputWindow()
    app.mainloop()


