import socket
import struct
import re,subprocess

DESTINATION = "ff:ff:ff:ff:ff:ff"


"""arg = list(), Tokenize HA and IP by delimeter . and : """
def Tokenizer(str1):
    if(str1.find(".")!=-1):
        list_split=[int(str1.split(".")[i],10) for i in range(0,4)]
    else:
        list_split=[int(str1.split(":")[i],16) for i in range(0,6)]
    return list_split

"""RAW socket Shooter, BROADCAST is available and you can also reuse addr to bind socket"""
def ARP_shoot(ARP_,device):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    sock.bind((device, 0))
    sock.send(b''.join(ARP_))
    sock.close()

"""ARP FRAME Struct made with struct lib"""
def ARP_Pack(desitination,source,option,sender_HA,sender_IP,target_HA,target_IP):
    if(option=="ARP_REQUEST"):
        option=1
        target_HA=Tokenizer("00:00:00:00:00:00")
    else:
        option=2
    ARP_ = [
        struct.pack('!6B',*desitination),#FF*6
        struct.pack('!6B',*source),#uuid
        struct.pack('!H',0x0806),#ARP
        struct.pack('!H',0x0001),#Ethernet
        struct.pack('!H',0x0800),#IPv4
        struct.pack('!B',0x06),#Hardware size
        struct.pack('!B',0x04),#Protocol size
        struct.pack('!H',option),#request:1,reply:2
        struct.pack('!6B',*sender_HA),#sender_mac
        struct.pack('!4B',*sender_IP),#sender_ip
        struct.pack('!6B',*target_HA),#Target_mac
        struct.pack('!4B',*target_IP)#Target_ip
        ]
    return ARP_

"""Parese HA on ifconfig output by using REGEX"""
def mac_get(device):
    out = re.findall("ether ([0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2}:[0-9a-z]{2})",subprocess.check_output(["ifconfig",device]))[0]
    return out

"""Parese IP on ip address show output by using REGEX"""
def ip_get(device):
    out = re.findall("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/24",subprocess.check_output(["ip","address","show",device]))[0]
    return out

"""Parese device list on ip link show output by using REGEX"""
def device_get():
    out = re.findall(":\s(\S*?):",subprocess.check_output(["ip","link","show"]))
    del(out)[0]
    return out


