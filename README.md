# Lab 05: Dissecting Internet paths

## Overview
Traffic is routed within and across autonomous systems (ASes) based on AS policies and the relationships between ASes. In this lab, you’ll explore the logical and geographical paths that are currently used to reach various destinations around the world. 

### Learning objectives
After completing this lab, you should be able to:
* Use `paris-traceroute` to discover the network path to a particular destination
* Use `whois` to lookup IP address to AS mappings
* Summarize the logical and geographical path used to reach a destination

## Getting started
Clone your git repository on the `tigers` servers. Your repository contains:
* `docker_traceroute.sh` — a script to run `paris-traceroute` in a Docker image
* `traceroute_data/google.txt` — sample output from paris-traceroute for google.com
* `path.py` — a partially written Python program for analyzing paris-traceroute’s output
* `questions.md` — a file of questions for you to answer

## Part 1: Tracing paths
Your first task is to determine the paths (i.e., sequence of routers) used to reach various destinations around the world. To accomplish this task, you will run `paris-traceroute` within a Docker container. (If you want to know how Paris traceroute works, you can read this paper after lab: Brice Augustin et al. Avoiding traceroute anomalies with Paris traceroute. In _Internet Measurement Conference (IMC)._ 2006. [https://conferences.sigcomm.org/imc/2006/papers/p15-augustin.pdf](https://conferences.sigcomm.org/imc/2006/papers/p15-augustin.pdf))

You can run `paris-traceroute` in Docker using the `docker_paris.sh` script included in your git repo. For example, to determine the path from the Computer Science department to Rochester Institute of Technology (RIT), run:
```bash
./docker_traceroute.sh cs.rit.edu 
```

You should see output similar to the following:

```
traceroute to cs.rit.edu (129.21.30.104), 30 hops max, 30 bytes packets
 1  172.17.0.1 (172.17.0.1)  0.024ms    0.023ms    0.019ms  
 2  vlan0080-hsrp-1.colgate.edu (149.43.80.2)  0.735ms    0.736ms    0.738ms  
 3  10.9.52.10 (10.9.52.10)  0.821ms    0.824ms    0.829ms  
 4  172.16.1.12 (172.16.1.12)  1.055ms    1.807ms    1.808ms  
 5  syr-9208-colgate.nysernet.net (199.109.9.57)  1.324ms    2.146ms    2.146ms  
 6  buf-9208-syr-9208.nysernet.net (199.109.7.194)  4.478ms    4.482ms    4.485ms  
 7  rit-buf-9208.nysernet.net (199.109.11.10)  6.168ms    6.175ms    6.180ms  
 8  rit-rtr001-pp-rit1-100g-vlan856.rit.edu (129.21.8.125)  6.709ms    7.709ms    7.714ms  
 9  rit-rtr070-pp-rtr001-vlan852.rit.edu (129.21.8.114)  10.628ms    11.691ms    11.694ms  
10  spidey.cs.rit.edu (129.21.30.104)  6.008ms    6.015ms    6.019ms  
```

Use `paris-traceroute` to determine the network paths from your Docker container to the following destinations. Store the output in a file by appending the file redirection operator (`>`) and a filename to the command. Store your files in your git repo in a directory called `traceroute_data`. 
**Domain name**    | **Filename**
-------------------|--------------
`cs.williams.edu`  | `williams.txt`
`cs.nyu.edu`       | `nyu.txt`
`bowdoin.edu`      | `bowdoin.txt`
`cs.uchicago.edu`  | `uchicago.txt`
`cs.carleton.edu`  | `carleton.txt`
`cs.hmc.edu`       | `harveymudd.txt`
`uow.edu.au`       | `wollongong.txt`
`tu.berlin`        | `tuberlin.txt`

🛑 **Commit and push your traceroute data to GitHub**

## Part 2: Autonomous system (AS) path
Your second task is to determine the sequence of autonomous systems (ASes) a path traverses. 

Many services exist to map IPs to ASes, including [Team Cymru's IP to ASN Mapping Service ](https://team-cymru.com/community-services/ip-asn-mapping/#whois), [Hacker Target's Autonomous System Lookup](https://hackertarget.com/as-ip-lookup) and [Frank Dennis's IPtoASN](https://iptoasn.com). We will use the last option, because it correctly analyzes NYSERnet IPs, whereas the first option does not and the section option offers to application programming interface (API).

Your git repo includes a partially written Python program (`path.py`) that:
1. Reads a file containing the output of `paris-traceroute` for a specific destination (see the `parse_file` and `parse_line` functions)
2. Outputs the IP addresses and hostsnames of the routers in the path (see the `summarize_path` function)

You can run the program as follows:
```
./path.py -f FILENAME
```
replacing `FILENAME` with the name of a file containing the output of `paris-traceroute` for a specific destination (e.g., `traceroute_data/google`)

Your task is to **write the `get_ASes` function**. You will need to use the [Python requests library](https://docs.python-requests.org/en/latest) to issue an HTTP request to the IPtoASN server running on `javan.cs.colgate.edu` on port `53661`. The HTTP response will contain a JavaScript Object Notation (JSON) message with data about the AS associated with an IP. For example, `http://javan.cs.colgate.edu:53661/v1/as/ip/149.43.80.2` will lookup the AS information for the IP address `149.43.80.2` and provide the following response: 
```
{
   "announced":true,
   "as_country_code":"US",
   "as_description":"COLGATE-UNIVERSITY - Colgate University",
   "as_number":1289,
   "first_ip":"149.43.0.0",
   "ip":"149.43.80.2",
   "last_ip":"149.43.255.255"
}
```
The get_ASes function should return a list of tuples, where each tuple contains an AS number and an AS name: e.g., `(1298, 'COLGATE-UNIVERSITY')`. If an IP address does not belong to an AS (e.g., IP addresses in the private address space 172.0.0.0/16), then skip this address. If a sequence of routers have IPs from the same AS, the AS should only be included once.

For example, when you run `path.py` with `traceroute_data/rit.txt`, the program should output:

```
ASes (3)
        1289    COLGATE-UNIVERSITY - Colgate University
        3754    NYSERNET3-AS - NYSERNet
        4385    RIT-ASN - Rochester Institute of Technology
```

## Part 3: Analyzing network paths

Your last task is to use your traceroute output from [Part 1](#part-1-tracing-paths) and your completed Python program from [Part 2](#part-2-autonomous-system-as-path) to answer the Part 3 questions in `questions.md`.

Note that router hostnames often contain identifiers (e.g., airport codes, city or state abbreviations, etc.) that indicate a router’s approximate geographic location.  For example, consider the hostnames of the routers in the path from your Docker container to Rochester Institute of Technology (RIT):
```
vlan0080-hsrp-1.colgate.edu
syr-9208-colgate.nysernet.net
buf-9208-syr-9208.nysernet.net
rit-buf-9208.nysernet.net
rit-rtr001-pp-rit1-100g-vlan856.rit.edu
rit-rtr070-pp-rtr001-vlan852.rit.edu
spidey.cs.rit.edu
```
The keywords `syr` and `buf` correspond to the cities Syracuse, NY and Buffalo, NY.

🛑  **Answer the Part 3 questions in `questions.md`**

## Submission instructions

When you are done, you should commit and push your changes to `path.py` and `questions.md` to GitHub.
