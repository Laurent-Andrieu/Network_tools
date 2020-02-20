from tkinter import *
from tkinter import ttk
import Netscan
from netaddr import IPAddress

selected = None


def config():
    res = [i for i in Netscan.get_config()]
    return res


def interface_callback():
    global selected
    params.config(state=NORMAL)
    params.delete('1.0', END)
    selected_interface = interface_list.selection_get()
    selected = selected_interface
    for interface in Netscan.get_config():
        if interface['interf'] == selected_interface:
            for k, v in interface.items():
                if k == 'ipv6':
                    params.insert(END, f'{k}:\t{v[-1]}\n')
                elif k == 'interf':
                    pass
                else:
                    params.insert(END, f'{k}:\t{v[0]}\n')
    params.config(state=DISABLED)


def scanner_callback():
    global selected
    scan_list.config(state=NORMAL)
    selected_interface = interface_list.selection_get()
    for interface in Netscan.get_config():
        if interface['interf'] == selected_interface and selected:
            netmask_bit = str(IPAddress(interface["netmask"][0]).netmask_bits())
            ip4 = interface['ipv4']
            for items in Netscan.scan(ip4[0] + '/' + netmask_bit):
                scan_list.insert(END, str(','.join(f'{key}={value}' for key, value in items.items())))


#   Root
root = Tk()
root.geometry('650x270')
#   -Frames: parent=root
global_frame = Frame(root)
global_frame.pack(side=LEFT)
#   -Notebooks: parent=frame
nb = ttk.Notebook(global_frame)
nb.pack(side=LEFT)
tab_names = ['Settings', 'Network Scanning', 'Arp Cache Poisoning']
tab = [ttk.Frame(nb) for notebook_tab in range(3)]
for i in range(3):
    nb.add(tab[i], text=tab_names[i])
nb.select(tab[0])
nb.enable_traversal()

#   -Sub-Frames: parents=notebooks tab1
tab_frame1 = Frame(tab[0])
tab_frame1.pack(side=LEFT)
tab_frame2 = Frame(tab[0])
tab_frame2.pack(side=RIGHT)
#   -Sub-Frames: parents=notebooks tab2
tab_frame3 = Frame(tab[1])
tab_frame3.pack(side=LEFT)
tab_frame4 = Frame(tab[1])
tab_frame4.pack(side=RIGHT)

#   -Widgets: Interface selection
interface_scrollbar = Scrollbar(tab_frame2)
interface_scrollbar.pack(side=RIGHT, fill=Y)
interface_label = Label(tab_frame1, text='Interfaces')
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

#   -Widgets: Application selection 1
scan_label = Label(tab_frame3, text='Here you can check all the machines\nconnected on the same network than yours')
scan_label.pack(side=TOP)
scan = Button(tab_frame3, text='Scan Network', command=scanner_callback, width=17, bd=4, relief='raised')
scan.pack(side=BOTTOM)
scan_scrollbar = Scrollbar(tab_frame4)
scan_scrollbar.pack(side=RIGHT, fill=Y)
scan_list = Listbox(tab_frame4, yscrollcommand=scan_scrollbar.set, state=DISABLED, width=40, height=50)
scan_list.pack()
scan_scrollbar.config(command=scan_list.yview)

mainloop()
