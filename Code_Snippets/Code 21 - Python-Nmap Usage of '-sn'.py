import nmap

# Initialize a Nmap PortScanner
scanner = nmap.PortScanner()
scanner.scan('127.0.0.1-3', arguments="-sn")
