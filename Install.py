#!/usr/bin/env python3
# -*-coding: utf-8-*-


import subprocess
import sys


try:
    import netfilterqueue
    import scapy.all
    import tkinter
    import optparse
    import re
except ImportError as err:
    print(err)
    subprocess.call('pip3 install NetfilterQueue', shell=True)
    subprocess.call('pip3 install scapy', shell=True)
    subprocess.call('pip3 install python3-tk', shell=True)
    subprocess.call('pip3 install optparse', shell=True)
    subprocess.call('pip3 install re', shell=True)

    if err:
        sys.stdout.write('Installation failed.\nRetry installation of the requirements manually')
    else:
        sys.stdout.write('Installation of modules completed!\nYou may no use the rest of the program.')
    sys.exit()
