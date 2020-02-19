from tkinter import *
from tkinter import ttk
import Netscan


def config():
    res = [i for i in Netscan.get_config()]
    return res


def interface_callback():
    params.config(state=NORMAL)
    params.delete('1.0', END)
    selected_interface = interface_list.selection_get()
    for interface in Netscan.get_config():
        if interface['interf'] == selected_interface:
            for k, v in interface.items():
                if k == "ipv6":
                    params.insert(END, f'{k}:\t{v[-1]}\n')
                elif k == "interf":
                    pass
                else:
                    params.insert(END, f'{k}:\t{v[0]}\n')
    params.config(state=DISABLED)


root = Tk()
global_frame = Frame(root)
global_frame.pack(side=LEFT)

nb = ttk.Notebook(global_frame)
nb.pack(side=LEFT)
tab1 = ttk.Frame(nb)
tab2 = ttk.Frame(nb)
nb.add(tab1, text="Paramètres")
nb.add(tab2, text="Applications")
nb.select(tab1)
nb.enable_traversal()

tab_frame1 = Frame(tab1)
tab_frame1.pack(side=LEFT)
tab_frame2 = Frame(tab1, bg="red")
tab_frame2.pack(side=RIGHT)

interface_scrollbar = Scrollbar(tab_frame2)
interface_scrollbar.pack(side=RIGHT, fill=Y)
interface_label = Label(tab_frame1, text="Interfaces")
interface_label.pack()
interface_list = Listbox(tab_frame1, yscrollcommand=interface_scrollbar.set)
config_len = 0
for a in range(len(config())):
    if not config()[a]['interf'] == 'lo':
        interface_list.insert(END, f'{config()[a]["interf"]}')
        config_len += 1
interface_list.config(height=str(config_len))
interface_list.pack()
bt_select = Button(tab_frame1, text='Select', command=interface_callback, width=17)
bt_select.pack()
interface_scrollbar.config(command=interface_list.yview)
params = Text(tab_frame2, height=10, width=50, state=DISABLED, wrap=WORD)
params.pack(side=RIGHT)

mainloop()