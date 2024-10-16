from scapy.all import *
from scapy.layers.inet import IP, ICMP

# Send an IP packet to the localhost and receive the response
response = sr1(IP(dst="127.0.0.1") / ICMP(), timeout=2)

# Check if a response was received
if response:
    print("Received response:")
    response.show()
else:
    print("No response received.")
