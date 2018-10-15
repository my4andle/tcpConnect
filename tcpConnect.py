#!/usr/bin/python3
"""
Usage:
  tcp_connect.py -h | --help
  tcp_connect.py (--target=<target> --port_count=<port_count>) [--timeout=<timeout>]

Options:
  --target=<target>         target
  --port_count=<port_count> port count default 65535
  --timeout=<timeout>       timeout for each tcp connection attempt
"""
import socket
from docopt import docopt
import concurrent.futures


def tcp_connect(target, port, timeout=1):
    """
    Generate a list of URLs from a given subnet in CIDR notation

    Args:
        subnet: A subnet in CIDR notation ex. 192.168.1.0/24

    Returns:
        List of IPv4 addresses
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((target, port))
        print("connected: {}:{}".format(target,port))
        return "{}:{}".format(target,port)
    except:
        print("failed: {}:{}".format(target,port))
        pass

def tcp_connect_concurrent(target, port_count):
    """
    Concurrently test tcp connections

    Args:
        target: target ipv4 address
        port_count: The number of ports to test starting at 1

    Returns:
        List of successful ports
    """
    results_list = []
    port_count = int(port_count)
    if port_count < 0:
        port_count = 1000
    elif port_count > 65535:
        port_count = 65535
    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as pool:
        results = {pool.submit(tcp_connect, target, port): port for port in range(port_count)}
        for future in concurrent.futures.as_completed(results):
            if future.result():
                results_list.append(future.result())
    return results_list

def main():
    opts = docopt(__doc__)
    if opts['--timeout']:
        res = tcp_connect_concurrent(opts['--target'], opts['--port_count'], opts['--timeout'])
    else:
        res = tcp_connect_concurrent(opts['--target'], opts['--port_count'])
    print(res)

if __name__ == '__main__':
    main()
