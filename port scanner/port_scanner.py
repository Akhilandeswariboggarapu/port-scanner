import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

# Argument Parser
parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
parser.add_argument("target", help="Target IP address or domain to scan")
parser.add_argument("-p", "--ports", help="Ports to scan, e.g., 22,80,443", default="22,80,443,3389,21")
args = parser.parse_args()

target = args.target
ports = [int(p.strip()) for p in args.ports.split(",")]

# Scanner function
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
        else:
            print(f"[-] Port {port} is CLOSED")
        sock.close()
    except socket.gaierror:
        print("[-] Hostname could not be resolved.")
    except socket.error:
        print("[-] Couldn't connect to server.")
    except KeyboardInterrupt:
        print("[-] User interrupted.")
        exit()

# Run with ThreadPoolExecutor for speed
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scan_port, ports)
