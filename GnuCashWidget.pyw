from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from GnuCashConverter import *

class GnuCashWidget(ttk.Frame):
    # manages the user interface

    def __init__(self, root):
        ttk.Frame.__init__(self, root)

        self.source_file     = StringVar()
        self.target_file     = StringVar()
        self.bank            = StringVar()
        self.initial_balance = StringVar()
        self.final_balance   = StringVar()
        self.message         = StringVar()

        root.title("GnuCash Converter")

        self.build_widget(root)

    def build_widget(self, root):
        main_widget = self.build_main_widget(root)

        self.message = ttk.Label(main_widget, text="")
        self.message.grid(column=1, row=1, sticky=(W, E))

        source_file_entry = ttk.Entry(main_widget, width=20, textvariable=self.source_file)
        source_file_entry.grid(column=1, row=2, sticky=(W, E))
        source_file_entry.focus()

        ttk.Button(main_widget, text='source file', command=self.askopenfile).grid(column=2, row=2)
        ttk.Entry(main_widget, width=20, textvariable=self.target_file).grid(column=1, row=3, sticky=(W, E))
        ttk.Button(main_widget, text="target file", command=self.asksavefile).grid(column=2, row=3)
        lst1 = ['rabobank','ing']
        ttk.OptionMenu(main_widget,self.bank,*lst1).grid(column=1, row=4)
        ttk.Label(main_widget, text="bank").grid(column=2, row=4, sticky=(W,E))
        ttk.Entry(main_widget, width=7, textvariable=self.initial_balance).grid(column=1, row=5, sticky=E)
        ttk.Label(main_widget, text="starting balance").grid(column=2, row=5, sticky=(W,E))
        ttk.Entry(main_widget, width=7, textvariable=self.final_balance).grid(column=1, row=6, sticky=E)
        ttk.Label(main_widget, text="final balance").grid(column=2, row=6, sticky=(W,E))
        ttk.Button(main_widget, text="Convert", command=self.convert).grid(column=2, row=7)
        ttk.Button(main_widget, text="Close", command=self.stop).grid(column=1, row=7)

        for child in main_widget.winfo_children(): child.grid_configure(padx=5, pady=5)

    def build_main_widget(self, root):
        main_widget = ttk.Frame(root, padding="3 3 12 12")
        main_widget.grid(column=0, row=0, sticky=(N, W, E, S))
        main_widget.columnconfigure(0, weight=1)
        main_widget.rowconfigure(0, weight=1)

        return main_widget

    def askopenfile(self):
        options = {
            'defaultextension': '.csv',
            'filetypes': [('all files', '.*'), ('text files', '.csv')],
            'initialdir': 'C:\\home\\2016',
            'title': 'open the source rabobank export file'
        }

        filename = filedialog.askopenfilename(**options)

        self.source_file.set(filename)

    def asksavefile(self):
        options = {
            'defaultextension': '.csv',
            'filetypes': [('text files', '.csv')],
            'initialdir': 'C:\\coding\\python',
            'title': 'file to save to'
        }

        filename = filedialog.asksaveasfilename(**options)

        self.target_file.set(filename)

    def convert(self):
        converter.convert(self.source_file.get(), self.target_file.get(), self.bank.get(), self.initial_balance.get(), self.final_balance.get())

        self.message['text'] = 'conversion succesfull'

    def stop(self):
        root.destroy()

if __name__ == '__main__':
  root = Tk()
  GnuCashWidget(root)
  root.mainloop()
