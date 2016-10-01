from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import constants
from decimal import *
from rabo2gnuCash import *

class raboWidget(ttk.Frame):
    # manages the user interface

    def __init__(self, root):
        # initialise parent class
        ttk.Frame.__init__(self, root)

        # source file to convert
        self.source_file = StringVar()

        # file to save convertion
        self.target_file = StringVar()

        # starting balance
        self.initial_balance = StringVar()

        # final balance
        self.final_balance = StringVar()

        # wisget messages
        self.message = StringVar()

        self.buildWidget(root);

    def buildWidget(self, root):
        # build the widget

        root.title("Rabobank to GnuCash Converter")

        # basic positioning and layout stuff
        main_widget = ttk.Frame(root, padding="3 3 12 12")
        main_widget.grid(column=0, row=0, sticky=(N, W, E, S))
        main_widget.columnconfigure(0, weight=1)
        main_widget.rowconfigure(0, weight=1)

        self.message = ttk.Label(main_widget, text="")
        self.message.grid(column=1, row=1, sticky=(W, E))

        source_file_entry = ttk.Entry(main_widget, width=20, textvariable=self.source_file)
        source_file_entry.grid(column=1, row=2, sticky=(W, E))
        source_file_entry.focus()
        ttk.Button(main_widget, text='source file', command=self.askopenfile).grid(column=2, row=2)

        ttk.Entry(main_widget, width=20, textvariable=self.target_file).grid(column=1, row=3, sticky=(W, E))
        ttk.Button(main_widget, text="target file", command=self.asksavefile).grid(column=2, row=3)

        ttk.Entry(main_widget, width=7, textvariable=self.initial_balance).grid(column=1, row=4, sticky=E)
        ttk.Label(main_widget, text="starting balance").grid(column=2, row=4, sticky=(W,E))

        ttk.Entry(main_widget, width=7, textvariable=self.final_balance).grid(column=1, row=5, sticky=E)
        ttk.Label(main_widget, text="final balance").grid(column=2, row=5, sticky=(W,E))

        ttk.Button(main_widget, text="Convert", command=self.convert).grid(column=2, row=6)

        for child in main_widget.winfo_children(): child.grid_configure(padx=5, pady=5)

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

        self.source_file.set(filename)

    # ask for the target directory
    def asksavefile(self):
        options = {
            'defaultextension': '.csv',
            'filetypes': [('all files', '.*'), ('text files', '.csv')],
            'initialdir': 'C:\\coding\\python',
            'title': 'file to save to'
        }

        # validate

        self.target_file.set(filedialog.asksaveasfilename(**options))

    def convert(self):
        converter = rabo2gnuCash()
        converter.convert(self.source_file.get(), self.target_file.get(), self.initial_balance.get(), self.final_balance.get())

        self.message['text'] = 'conversion succesful'


if __name__ == '__main__':
  root = Tk()
  raboWidget(root)
  root.mainloop()
