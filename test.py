from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
import Netscan
from netaddr import IPAddress

def config():
    res = [i for i in Netscan.get_config()]
    return res


def display_info(info):
    filewin = Toplevel(root)
    button = Button(filewin, textvariable="")
    button.pack()


def interface_callback():
    params.config(state=NORMAL)
    params.delete('1.0', END)
    selected = interface_list.selection_get()
    for interface in Netscan.get_config():
        if interface['interf'] == selected:
            params.insert(END, str('\n'.join(f'{k}:\t{v}' for k, v in interface.items())))
    params.config(state=DISABLED)


def scanner_callback():
    users.config(state=NORMAL)
    selected = interface_list.selection_get()
    for interface in Netscan.get_config():
        if interface['interf'] == selected:
            netmask_bit = str(IPAddress(interface["netmask"][0]).netmask_bits())
            ip4 = interface['ipv4']
            for items in Netscan.scan(ip4[0] + '/' + netmask_bit):
                users.insert(END, str(''.join(f'{ip}\t{mac}\n' for ip, mac in items.items())))

# TODO: Créer fenetre démarrage sudo
# ROOT
root = Tk()
root.geometry("800x300")
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
main = Frame(root, bg="#d6c4c3", bd=3)
main.pack(side=TOP, fill=X)
interface_frame = Frame(main, bg='#d6c4c3', bd=3, height=150, width=300)
interface_frame.pack(side=LEFT)
info_frame = Frame(main, bg='#d6c4c3', bd=3, height=300, width=300)
info_frame.pack(side=LEFT)
scanner_frame = Frame(main, bg="#d6c4c3", bd=3, height=200, width=450)
scanner_frame.pack(side=LEFT)

#   WINDOW
#window1 = ttk.Notebook(main)
#tab1 = ttk.Frame(main)
#window1.add(main, text='Paramétrage',)
#window1.pack(side=LEFT, fill=BOTH)

#   Label
interface_label = Label(interface_frame, text='Interfaces', bg='#d6bebc', fg='#108187')
interface_label.pack()

#   Interfaces Widget
interface_scrollbar = Scrollbar(interface_frame)
interface_scrollbar.pack(side=RIGHT, fill=Y)
interface_list = Listbox(interface_frame, yscrollcommand=interface_scrollbar.set)
for a in range(len(config())):
    if not config()[a]['interf'] == 'lo':
        interface_list.insert(END, f'{config()[a]["interf"]}')
interface_list.pack(side=LEFT, fill=BOTH)
interface_scrollbar.config(command=interface_list.yview)

#   Interface info Widgets
bt_select = Button(info_frame, text='Select', command=interface_callback)
bt_select.pack()
params = Text(info_frame, height=10, width=45, state=DISABLED, wrap=WORD)
params.pack()

#   Network scanner Widget
bt_scan = Button(scanner_frame, text='Scan', command=scanner_callback)
bt_scan.pack()
scanner_scrollbar = Scrollbar(scanner_frame)
scanner_scrollbar.pack(side=RIGHT, fill=Y)
users = Listbox(scanner_frame, yscrollcommand=scanner_scrollbar.set, height=12, width=60)
users.pack(side=LEFT, fill=BOTH)

# ROOT-END
root.config(menu=menubar, bg="white")
root.mainloop()
