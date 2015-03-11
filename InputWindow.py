import Tkinter as tk
import ProcessStats


class InputWindow(tk.Frame):

    def __init__(self, master=None):
        self.createWindow(master)
        self.populateObjects()


    def createWindow(self, master):
        tk.Frame.__init__(self, master)
        self.grid()


    def populateObjects(self):
        self.createTextEntry()
        self.createSubmitButton()
        self.createCancelButton()

    def createSubmitButton(self):
        self.submitButton = tk.Button(self, text='Submit', command=self.submitFile)
        self.submitButton.grid(row=0, column=1)


    def createCancelButton(self):
        self.cancelButton=tk.Button(self, text='Cancel', command=self.quit)
        self.cancelButton.grid()


    def createTextEntry(self):
        self.textEntry=tk.Entry(self, exportselection=0)
        self.textEntry.grid(row=0, column=0)
        self.textEntry.insert(0,'Enter a filename')



    def submitFile(self):
        f = self.textEntry.get()
        ProcessStats.main([None, f])
        
        
if __name__ == '__main__':
    app = InputWindow()
    app.master.title('test')
    app.mainloop()


