#!/usr/bin/env python3
# -*-coding: utf-8-*-


import re
import subprocess
import scapy.all as scapy


def get_config():

    int_cmd = subprocess.check_output('ip link show', shell=True)
    interfaces = re.findall('\d+: (\w+)', str(int_cmd))
    interface = []

    for i, interf in enumerate(interfaces):
        cfg_cmd = subprocess.check_output(f'ifconfig {interf}', shell=True)
        cfg_cmd = str(cfg_cmd)
        mac = re.findall('ether ([\w{2}:]{17})', cfg_cmd)
        ipv6 = re.findall('inet6 ([\w+:]+)', cfg_cmd)
        ipv4 = re.findall('inet ([\d{3}.+]+)', cfg_cmd)
        broadcast = re.findall('broadcast ([\d{1,3}.]+)', cfg_cmd)
        netmask = re.findall('netmask ([\d{1,3}.]+)', cfg_cmd)

        if (mac, ipv4, ipv6, broadcast, netmask):
            interface.append({'interf': interf, 'mac': mac, 'ipv4': ipv4, 'ipv6': ipv6, 'netmask': netmask,
                              'broadcast': broadcast})
    return interface


def netscan(interfaces):
    net_interfaces = []
    for i in interfaces:
        for j in i:
            net_interfaces.append(i[f'{j}'])


netscan(get_config())
