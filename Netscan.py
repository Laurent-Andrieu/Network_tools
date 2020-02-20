#!/usr/bin/env python3
# -*-coding: utf-8-*-

import re
import subprocess
import scapy.all as scapy


def get_config():
    int_cmd = subprocess.check_output('ip link show', shell=True)
    interfaces = re.findall('\d+: (\w+)', str(int_cmd))
    interface_list = []
    for i, interf in enumerate(interfaces):
        cfg_cmd = subprocess.check_output(f'ifconfig {interf}', shell=True)
        cfg_cmd = str(cfg_cmd)
        mac = re.findall('ether ([\w{2}:]{17})', cfg_cmd)
        ipv6 = re.findall('inet6 ([\w+:]+)', cfg_cmd)
        ipv4 = re.findall('inet ([\d{3}.+]+)', cfg_cmd)
        broadcast = re.findall('broadcast ([\d{1,3}.]+)', cfg_cmd)
        netmask = re.findall('netmask ([\d{1,3}.]+)', cfg_cmd)

        if (mac, ipv4, ipv6, broadcast, netmask):
            interface_list.append({'interf': interf, 'mac': mac, 'ipv4': ipv4, 'ipv6': ipv6, 'netmask': netmask,
                              'broadcast': broadcast})
    return interface_list


def scan(ipv4):
    arp_request = scapy.ARP(pdst=ipv4)
    broadcast = scapy.Ether(dst=b"ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answer = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients = [{"IP": address[1].psrc, "MAC": address[1].hwsrc} for address in answer]
    return clients


def get_gateway():
    gtw_cmd = subprocess.check_output('ip route show default 0.0.0.0/0', shell=True)
    gtw = re.search(r'([\d{3}.+]+).+(\b[\w|\d]+)(?:\sproto)', str(gtw_cmd)).groups()
    return gtw
