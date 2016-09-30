from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from decimal import *
from rabo2gnucashconverter import *

# ask for the source file
def askopenfile():
    options = {
        'defaultextension': '.csv',
        'filetypes': [('all files', '.*'), ('text files', '.csv')],
        'initialdir': 'C:\\home\\2016',
        'title': 'open the source rabobank export file'
    }
    
    source.set(filedialog.askopenfilename(**options))

# ask for the target directory
def asksavefile():
    options = {
        'defaultextension': '.csv',
        'filetypes': [('all files', '.*'), ('text files', '.csv')],
        'initialdir': 'C:\\coding\\python',
        'title': 'file to save to'
    }

    target.set(filedialog.asksaveasfilename(**options))

def convert():
    converter = rabo2gnucashconverter()
    converter.convert(source, target, startCum, endCum)

# build window
root = Tk()
root.title("Rabobank to GnuCash Converter")

# basic positioning and layout stuff
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# initiate vars
source   = StringVar()
target   = StringVar()
startCum = StringVar()
endCum   = StringVar()
messages = StringVar()

source_entry = ttk.Entry(mainframe, width=20, textvariable=source)
source_entry.grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text='source file', command=askopenfile).grid(column=3, row=2)

target_entry = ttk.Entry(mainframe, width=20, textvariable=target)
target_entry.grid(column=2, row=3, sticky=(W, E))
ttk.Button(mainframe, text="target file", command=asksavefile).grid(column=3, row=3, sticky=W)

startCum_entry = ttk.Entry(mainframe, width=7, textvariable=startCum)
startCum_entry.grid(column=2, row=4, sticky=(W, E))
ttk.Label(mainframe, text="starting balance").grid(column=3, row=4, sticky=W)

endCum_entry = ttk.Entry(mainframe, width=7, textvariable=endCum)
endCum_entry.grid(column=2, row=5, sticky=(W, E))
ttk.Label(mainframe, text="final balance").grid(column=3, row=5, sticky=W)

ttk.Label(mainframe, textvariable=messages).grid(column=2, row=1, sticky=(W, E))
ttk.Button(mainframe, text="Convert", command=convert).grid(column=3, row=7, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
source_entry.focus()

root.mainloop()