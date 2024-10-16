from scapy.all import *
from scapy.layers.inet import IP, ICMP
from scapy.layers.l2 import Ether

# Send an IP packet (layer 3 packet)
send(IP(dst="127.0.0.1")/ICMP())

# Send an Ethernet frame (layer 2 packet)
sendp(Ether(dst="ff:ff:ff:ff:ff:ff")/IP(dst="127.0.0.1")/ICMP())
