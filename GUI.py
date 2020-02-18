from tkinter import *
import Netscan


def config():
    res = []
    for i in Netscan.get_config():
        res.append(i)
    return res


def display_info(info):
    filewin = Toplevel(root)
    button = Button(filewin, text="")
    button.pack()


def callback():
    exam = interface_list.selection_get()
    for x in config():
        if x["interf"] == exam:
            var.set(f'{x}')


# ROOT
root = Tk()
root.geometry("500x500")
#   MENU
menubar = Menu(root, bg="white")
#       FILE
filemenu = Menu(menubar, tearoff=0, bg="white")
filemenu.add_command(label="Version", command=display_info)
filemenu.add_command(label="Credits", command=display_info)
filemenu.add_command(label="Close")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
#       HELP
helpmenu = Menu(menubar, tearoff=0, bg="white")
helpmenu.add_command(label="Help Index", command=display_info)
helpmenu.add_command(label="About...", command=display_info)
menubar.add_cascade(label="Help", menu=helpmenu)

# Frames
interface_frame = Frame(root, bg='#d6bebc', bd=3, height=150, width=300)
interface_frame.grid(row=0, column=0)
scanner_frame = Frame(root, bg='#d6c4c3', bd=3, height=300, width=300)
scanner_frame.grid(row=0, column=1)

#   Label
interface_label = Label(interface_frame, text='Interfaces', bg='#d6bebc', fg='#108187')
interface_label.pack()

#   Interfaces Widget
scrollbar = Scrollbar(interface_frame)
scrollbar.pack(side=RIGHT, fill=Y)
interface_list = Listbox(interface_frame, yscrollcommand=scrollbar.set)
for a in range(len(config())):
    if not config()[a]['interf'] == 'lo':
        interface_list.insert(END, f'{config()[a]["interf"]}')
interface_list.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=interface_list.yview)


#   Network Scanner Widget
var = StringVar()
bt = Button(scanner_frame, text='Scan', command=callback)
bt.pack()
result = Message(scanner_frame, textvariable=var, )
result.pack()
# ROOT-END
root.config(menu=menubar, bg="white")
root.mainloop()
