#!/usr/bin/env python
# *-utf-8-*

import subprocess
import sys

# TODO: Ajouter un 2nd exept avec git clone


try:
    import netfilterqueue
    import scapy.all
except ImportError as err:
    print(err)
    subprocess.call('pip3 install NetfilterQueue', shell=True)
    subprocess.call('pip3 install scapy', shell=True)
    if err:
        sys.stdout.write('Installation failed.\nRetry installation of the requirements manually')
    else:
        sys.stdout.write('Installation of modules completed!\nYou may no use the rest of the program.')
    sys.exit()
