from scapy.layers.inet import IP, TCP

# Custom IP and TCP packet
packet = IP(src="127.0.0.1", dst="127.0.0.2")/TCP(dport=80, flags="S")

# Display the packet
packet.show()
