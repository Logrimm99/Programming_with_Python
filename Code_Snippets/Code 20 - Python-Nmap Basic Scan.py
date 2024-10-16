import nmap

# Initialize a Nmap PortScanner
scanner = nmap.PortScanner()
ip_addr = '127.0.0.1'
port_range = '1-443'
# Scan the ports 1 to 443 of the IP address '127.0.0.1'
scanner.scan(ip_addr, port_range)
