from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import constants
from decimal import *
from rabo2gnucashconverter import *

class raboWidget(ttk.Frame):
    # manages the user interface

    def __init__(self, root):
        # initialise parent class
        ttk.Frame.__init__(self, root)

        # source file to convert
        self.source = StringVar()

        # file to save convertion
        self.target = StringVar()

        # starting balance
        self.initialBalance = StringVar()

        # final balance
        self.finalBalance = StringVar()

        # wisget messages
        self.message = StringVar()

        self.buildWidget(root);

    def buildWidget(self, root):
        # build the widget

        root.title("Rabobank to GnuCash Converter")

        # basic positioning and layout stuff
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.message = ttk.Label(mainframe, text="")
        self.message.grid(column=1, row=1, sticky=(W, E))

        source_entry = ttk.Entry(mainframe, width=20, textvariable=self.source)
        source_entry.grid(column=1, row=2, sticky=(W, E))
        source_entry.focus()
        ttk.Button(mainframe, text='source file', command=self.askopenfile).grid(column=3, row=2)

        ttk.Entry(mainframe, width=20, textvariable=self.target).grid(column=2, row=3, sticky=(W, E))
        ttk.Button(mainframe, text="target file", command=self.asksavefile).grid(column=3, row=3, sticky=W)

        ttk.Entry(mainframe, width=7, textvariable=self.initialBalance).grid(column=2, row=4, sticky=(W, E))
        ttk.Label(mainframe, text="starting balance").grid(column=3, row=4, sticky=W)

        ttk.Entry(mainframe, width=7, textvariable=self.finalBalance).grid(column=2, row=5, sticky=(W, E))
        ttk.Label(mainframe, text="final balance").grid(column=3, row=5, sticky=W)

        ttk.Button(mainframe, text="Convert", command=self.convert).grid(column=3, row=7, sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def askopenfile(self):
        # ask for the source file
        options = {
            'defaultextension': '.csv',
            'filetypes': [('all files', '.*'), ('text files', '.csv')],
            'initialdir': 'C:\\home\\2016',
            'title': 'open the source rabobank export file'
        }

        filename = filedialog.askopenfilename(**options)

        # validate

        self.source.set(filename)

    # ask for the target directory
    def asksavefile(self):
        options = {
            'defaultextension': '.csv',
            'filetypes': [('all files', '.*'), ('text files', '.csv')],
            'initialdir': 'C:\\coding\\python',
            'title': 'file to save to'
        }

        # validate

        self.target.set(filedialog.asksaveasfilename(**options))

    def convert(self):
        converter = rabo2gnucashconverter()
        converter.convert(self.source.get(), self.target.get(), self.initialBalance.get(), self.finalBalance.get())

        self.message['text'] = 'conversion succesful'


if __name__ == '__main__':
  root = Tk()
  raboWidget(root)
  root.mainloop()
