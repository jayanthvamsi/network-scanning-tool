import socket
import os
import ipaddress
from datetime import datetime
import concurrent.futures

# Function to get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

# Function to scan a range of ports on a given IP
def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

# Function to scan a list of IPs
def is_alive(ip):
    response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")
    if response==0:
        return ip
    else:
        return None

def scan_ips(ips):
    alive_ips = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(is_alive, ips))
    
    for ip in results:
        if ip is not None:
            alive_ips.append(ip)
    return alive_ips

def get_port_info(port):
    try:
        service_name = socket.getservbyport(port)
        protocol = socket.getservbyport(port)
        return {
            "Port": port,
            "Service Name": service_name,
            "STATE": "OPEN",
            "Protocol": protocol
        }
    except (socket.error, OSError):
        return {
            "Port": port,
            "Service Name": "Unknown",
            "STATE": "OPEN",
            "Protocol": "Unknown"
        }


def scan():
    # Ask for device port scan or list of hosts alive in the network
    option = input("Choose an option:\n1. Know my ip\n2. Device Port Scan\n3. List of Hosts Alive in the Network\n4. exit\n")

    if option == '1':

        local_ip = get_local_ip()
        print(f"Your IP address is: {local_ip}")
        scan()

    elif option =='2':

        ip_to_scan = input("Enter the IP address to scan: ")
        port_option = input("Choose a port scanning option:\n1. Scan a range of ports\n2. Scan custom ports\n3. Scan all ports\n")

        if port_option == '1':
            start_port, end_port = map(int, input("Enter the range of ports (start-end): ").split('-'))
            open_ports = scan_ports(ip_to_scan, range(start_port, end_port + 1))
            print(f"Scan report for {ip_to_scan}")
            response = os.system(f"ping -c 1 {ip_to_scan}")
            print(f"{response}")
            if response==0:
                print(f"Host is up")
                print("PORT      SERVICE   STATE     PROTOCOL")
                for open_port in open_ports:
                    port_info = get_port_info(open_port)
                    for service,value in port_info.items():
                        print(value,end=" "*(10-len(str(value))))
                    print()
            else:
                print(f"Host is down")

        elif port_option == '2':
            custom_ports = list(map(int, input("Enter custom ports (space-separated):").split()))
            open_ports = scan_ports(ip_to_scan, custom_ports)
            print(f"Scan report for {ip_to_scan}")
            response = os.system(f"ping -c 1 {ip_to_scan}")
            print(f"{response}")
            if response==0:
                print(f"Host is up")
                print("PORT      SERVICE   STATE     PROTOCOL")
                for open_port in open_ports:
                    port_info = get_port_info(open_port)
                    for service,value in port_info.items():
                        print(value,end=" "*(10-len(str(value))))
                    print()
            else:
                print(f"Host is down")

        elif port_option == '3':
            open_ports = scan_ports(ip_to_scan, range(1, 65536))
            print(f"Scan report for {ip_to_scan}")
            response = os.system(f"ping -c 1 {ip_to_scan}")
            print(f"{response}")
            if response==0:
                print(f"Host is up")
                print("PORT      SERVICE   STATE     PROTOCOL")
                for open_port in open_ports:
                    port_info = get_port_info(open_port)
                    for service,value in port_info.items():
                        print(value,end=" "*(10-len(str(value))))
                    print()
            else:
                print(f"Host is down")

        print()
        scan()
            
    elif option == '3':
        ip_option = input("Choose an IP scanning option:\n1. Scan a range of IPs\n2. Scan custom IPs\n3. Scan all IPs in the network\n")

        if ip_option == '1':
            start_ip, end_ip = input("Enter the range of IPs (start-end): ").split('-')
            ips_to_scan = [str(ip) for ip in ipaddress.IPv4Network(f'{start_ip}/{end_ip}', strict=False)]
            alive_ips = scan_ips(ips_to_scan)
            print("Alive IPs in the range:")
            for ip in alive_ips:
                print(ip)

        elif ip_option == '2':
            custom_ips = input("Enter custom IPs (space-separated): ").split()
            alive_ips = scan_ips(custom_ips)
            print("Alive custom IPs:")
            for ip in alive_ips:
                print(ip)

        elif ip_option == '3':
            local_ip = get_local_ip()
            local_network = ipaddress.IPv4Network(f'{local_ip}/24', strict=False)
            ips_to_scan = [str(ip) for ip in local_network]
            alive_ips = scan_ips(ips_to_scan)
            print("Alive IPs in the local network:")
            for ip in alive_ips:
                print(ip)
        
        scan()

    elif option =='4':
        return 0

if __name__=='__main__':
    scan()
