#!/usr/bin/env python3

from argparse import ArgumentParser
import socket

def parse_file(filepath):
    """Parses a file containing output from paris-traceroute and returns a 
    list of router addresses
    """
    with open(filepath) as datafile:
        lines = datafile.readlines()

    datalines = lines[1:-1]
    path = [parse_line(line) for line in datalines]
    path = [node for node in path if node != None]
    return path

def parse_line(line):
    """Parses a single line of output from paris-traceroute"""
    # Ensure it is a hop line
    line = line.strip()
    if line.startswith("MPLS"):
        return None
   
    # Break line into parts 
    parts = line.split(' ')
    parts = [part for part in parts if part !='']
    hostname = parts[1]
    ip = parts[2].strip('()')

    # Return hostname and IP address
    if hostname == ip:
        hostname = None
    if ip == "*":
        return None
    return (ip, hostname)

def get_ASes(hops):
    """Converts a list of (Internet Protocol address, hostname) tuples to a list of (autonomous system number, autonomous system name) tuples"""
    ASes = []

    # TODO

    return ASes

def summarize_path(hops):
    """Output IP, hostnames, and ASes in path"""
    print("Routers ({})".format(len(hops)))
    print('\t' + '\n\t'.join(["{}\t{}".format(ip, ("" if hostname is None else hostname)) for ip, hostname in hops]))
    ases = get_ASes(hops)
    print("ASes ({})".format(len(ases)))
    print('\t' + '\n\t'.join(["{}\t{}".format(asn, name) for asn, name in ases])) 

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Analyze Internet path')
    arg_parser.add_argument('-f', '--filepath', dest='filepath', action='store',
            required=True, 
            help='Path to file with paris-traceroute output')
    settings = arg_parser.parse_args()

    path = parse_file(settings.filepath)
    summarize_path(path)

if __name__ == '__main__':
    main()
