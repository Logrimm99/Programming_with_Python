import nmap

# Initialize a Nmap PortScanner
scanner = nmap.PortScanner()
scanner.scan('127.0.0.1-6', arguments='-sA -top-ports 100')

for host in scanner.all_hosts():
    print('-' * 35)
    print('Host: ', host)
    print('State: ', scanner[host].state())
    for protocol in scanner[host].all_protocols():
        print('Protocol:', protocol)
        ports = scanner[host][protocol].keys()
        for port in ports:
            print('port: ', port, ' state: ', scanner[host][protocol][port]['state'])
