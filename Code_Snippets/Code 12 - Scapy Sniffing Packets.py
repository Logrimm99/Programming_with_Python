from scapy.all import *

# Sniff for IP packets
packets = sniff(filter="ip", count=10)

# Display the captured packets
packets.summary()
