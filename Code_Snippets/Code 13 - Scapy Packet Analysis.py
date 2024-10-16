from scapy.all import *
from scapy.layers.inet import IP

# Sniff and save packets to a .pcap file
captured_packets = sniff(count=100)
wrpcap("captured_packets.pcap", captured_packets)

# Load packets from a .pcap file
loaded_packets = rdpcap("captured_packets.pcap")

# Count the amount of packets received per source IP address
ip_counts = {}
for pkt in loaded_packets:
    if IP in pkt:
        src_ip = pkt[IP].src
        if src_ip in ip_counts:
            ip_counts[src_ip] += 1
        else:
            ip_counts[src_ip] = 1

print(ip_counts)

# Find the source IP address the least packets were received from (still at least one)
ip_counts_list = list(ip_counts.items())
ip_counts_list.sort(key=lambda x: x[1])

# Filter the packets based on the least occurring source IP address
filtered_packets = [pkt for pkt in loaded_packets if IP in pkt and pkt[IP].src == ip_counts_list[0][0]]

# Print the payloads of the filtered packets
for pkt in filtered_packets:
    if Raw in pkt:
        payload = pkt[Raw].load
        print ('Payload:', payload)
