from scapy.layers.inet import IP, ICMP

# Create an IP packet with the localhost as destination
ip_packet = IP(dst="127.0.0.1")/ICMP()

# Display the packet
ip_packet.show()
