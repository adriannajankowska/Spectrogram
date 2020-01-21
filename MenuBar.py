from tkinter import *

class MenuBar:
    def __init__(self, root):
        self.root = root

        self.FileNew_Callback = self.Empty_Callback
        self.FileOpen_Callback = self.Empty_Callback
        self.FileSave_Callback = self.Empty_Callback


    def Init(self):
        # File Menu
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.FileNew_Callback)
        self.filemenu.add_command(label="Open", command=self.FileOpen_Callback)
        self.filemenu.add_command(label="Save", command=self.FileSave_Callback)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close", command=self.root.quit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit Menu
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo", command=self.Empty_Callback)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", command=self.Empty_Callback)
        self.editmenu.add_command(label="Copy", command=self.Empty_Callback)
        self.editmenu.add_command(label="Paste", command=self.Empty_Callback)
        self.editmenu.add_command(label="Delete", command=self.Empty_Callback)
        self.editmenu.add_command(label="Select All", command=self.Empty_Callback)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # Help Menu
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.Empty_Callback)
        self.helpmenu.add_command(label="About...", command=self.Empty_Callback)

        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    def GetObject(self):
        return self.menubar

    def Empty_Callback(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()
