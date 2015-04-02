import Tkinter as tk
import ProcessStats
import SettingsWindow
import StatsParser
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
        self.textEntry=tk.Entry(self, exportselection=0, width=30)
        self.textEntry.grid(row=0, column=0,padx=10, pady=10)
        self.textEntry.insert(0,'Enter a filename or directory')



    def submitFile(self):
        f = self.textEntry.get()
        # don't take any action for no entry
        if(f == 'Enter a filename or directory') | (f==''): pass
        else: ProcessStats.process(f)

        
    def showSettings(self):
        self.settings=SettingsWindow.SettingsWindow()

'''
    # files: a list of file or directory names
    def processStats(self, f):
        if(os.path.isdir(f)): self.iterate_directory(f)
        else: 
            print("Processing " + f)
            StatsParser.processFile(f)
            
      #  else: print("unrecognized file type") #FIXME handle this more thoroughly
        
    def iterate_directory(self, path):        
        for dirpath, dirnames, files in os.walk(path):
            for f in files:
                try: data = open(os.path.join(dirpath,f), "r")
                except Exception, args: print(args) 
                else:
                    print("Processing " + f)
                    try: StatsParser.processFile(data)
                    except Exception, args: print(args)
                    finally: data.close()
'''

        
if __name__ == '__main__':
    app = InputWindow()
    app.mainloop()


