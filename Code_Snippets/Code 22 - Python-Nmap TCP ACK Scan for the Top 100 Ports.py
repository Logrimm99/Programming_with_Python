import nmap

# Initialize a Nmap PortScanner
scanner = nmap.PortScanner()
scanner.scan('127.0.0.1', arguments='-sA -top-ports 100')
