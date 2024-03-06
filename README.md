# Lab 06: Dissecting Internet paths

## Overview
Traffic is routed within and across autonomous systems (ASes) based on AS policies and the relationships between ASes. In this lab, you’ll explore the logical and geographical paths that are currently used to reach various destinations around the world. 

### Learning objectives
After completing this lab, you should be able to:
* Use `traceroute` to discover the network path to a particular destination
* Use `whois` to discover information about IP address ownership
* Summarize the logical and geographical path used to reach a destination

## Getting started
Clone your git repository on a `tigers` server. Your repository contains:
* `docker_traceroute.sh` — a script to run `paris-traceroute` in a Docker image
* `traceroute_data/google.txt` — sample output from paris-traceroute for google.com
* `path.py` — a partially written Python program for analyzing paris-traceroute’s output
* `questions.md` — a file of questions for you to answer

## Part 1: Tracing paths
Your first task is to determine the paths (i.e., sequence of routers) used to reach various destinations around the world. To accomplish this task, you will run `paris-traceroute` within a Docker container. (If you want to know how Paris traceroute works, you can read this paper after lab: Brice Augustin et al. Avoiding traceroute anomalies with Paris traceroute. In _Internet Measurement Conference (IMC)._ 2006. [https://conferences.sigcomm.org/imc/2006/papers/p15-augustin.pdf](https://conferences.sigcomm.org/imc/2006/papers/p15-augustin.pdf))

You can run `paris-traceroute` in Docker using the `docker_traceroute.sh` script included in your git repo. For example, to determine the path from the Computer Science department to Google, run:
```bash
./docker_traceroute.sh google.com 
```

You should see output similar to the following:
```
traceroute to google.com (142.250.80.78), 30 hops max, 30 bytes packets
 1  172.17.0.1 (172.17.0.1)  0.089ms    0.065ms    0.053ms  
 2  vlan0080-hsrp-1.colgate.edu (149.43.80.2)  0.785ms    0.776ms    0.775ms  
 3  10.9.52.10 (10.9.52.10)  0.847ms    0.855ms    1.587ms  
 4  edge-router-case-bgp.colgate.edu (172.16.1.11)  0.907ms    1.672ms    1.664ms  
 5  alb-9204-colgate-cdn.nysernet.net (199.109.108.41)  3.674ms    3.669ms    3.672ms  
 6  nyc-9208-alb-9204-cdn.nysernet.net (199.109.107.101)  6.865ms    6.864ms    6.870ms  
 7  nyc32-55a1-nyc32-9208-cdn.nysernet.net (199.109.107.202)  6.972ms    6.969ms    6.968ms  
 8  199.109.114.18 (199.109.114.18)  8.734ms    9.560ms    9.562ms  
 9  * * *
10  216.239.62.24 (216.239.62.24)  42.153ms    42.151ms    189.056ms  
11  192.178.108.18 (192.178.108.18)  7.805ms    7.810ms    39.508ms  
12  108.170.227.151 (108.170.227.151)  8.251ms    8.250ms    53.983ms  
13  209.85.255.53 (209.85.255.53)  7.543ms    7.545ms    7.550ms  
14  192.178.106.163 (192.178.106.163)  9.432ms    9.433ms    9.440ms  
15  142.251.65.101 (142.251.65.101)  7.259ms    7.261ms    7.266ms  
16  lga34s35-in-f14.1e100.net (142.250.80.78)  7.233ms    7.226ms    7.229ms
```

Use `paris-traceroute` to determine the network paths from your Docker container to the following destinations. Store the output in a file by appending the file redirection operator (`>`) and a filename to the command. Store your files in your git repo in a directory called `traceroute_data`. 
**Domain name**            | **Filename**
---------------------------|--------------
`mx-ext.syr.edu`           | `syracuse.txt`
`dns1.morrisville.edu`     | `morrisville.txt`
`search.mta.info`          | `mta.txt`
`cs.nyu.edu`               | `nyu.txt`
`pelican.cs.ucla.edu`      | `ucla.txt`
`ns.claremont.edu`         | `claremont.txt`
`uow.edu.au`               | `wollongong.txt`
`en-enc.gate.tu-berlin.de` | `tuberlin.txt`

🛑 **Commit and push your traceroute data to GitHub**

## Part 2: Autonomous system (AS) path
Your second task is to determine the sequence of autonomous systems (ASes) a path traverses. 

Many services exist to map IPs to ASes, including [Team Cymru's IP to ASN Mapping Service](https://team-cymru.com/community-services/ip-asn-mapping), [Hacker Target's Autonomous System Lookup](https://hackertarget.com/as-ip-lookup), [Frank Dennis's IPtoASN](https://iptoasn.com), and [American Registry for Internet Numbers (ARIN) Whois/Registration/Data Access Protocol (RDAP)](https://www.arin.net/resources/registry/whois/rdap/). We will use the last option, because it relies on an official registry of subnet ownership. The other services rely on observations of subnets advertised by ASes using the Border Gateway Protocol (BGP), which can be incomplete depending on the vantage points of the service.

Your git repo includes a partially written Python program (`path.py`) that:
1. Reads a file containing the output of `paris-traceroute` for a specific destination (see the `parse_file` and `parse_line` functions)
2. Outputs the IP addresses and hostsnames of the routers in the path (see the `summarize_path` function)

You can run the program as follows:
```
./path.py -f FILENAME
```
replacing `FILENAME` with the name of a file containing the output of `paris-traceroute` for a specific destination (e.g., `traceroute_data/google`)

Your task is to **write the `get_ASes` function**. You will need to use the [Python requests library](https://docs.python-requests.org/en/latest) to issue an HTTP request to the [ARIN's RDAP service](https://www.arin.net/resources/registry/whois/rdap/#ip-networks). 

A few **important notes about ARIN's RDAP servce**:
* You **must** add calls to `time.sleep` in your Python code to limit your query rate to 2 queries per second
* The query example listed in the documentation for ARIN's RDAP service is incorrect; the correct query URL is `https://rdap.arin.net/registry/ip/`. For example, `https://rdap.arin.net/registry/ip/149.43.80.3` will lookup the ownership information for the IP address `149.43.80.3`.
* The HTTP response will contain a JavaScript Object Notation (JSON) message with data about the AS associated with an IP. For example:

```
{{
  "rdapConformance" : [ "nro_rdap_profile_0", "rdap_level_0", "cidr0", "arin_originas0" ],
  "notices" : [ {
    "title" : "Terms of Service",
    "description" : [ "By using the ARIN RDAP/Whois service, you are agreeing to the RDAP/Whois Terms of Use" ],
    "links" : [ {
      "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
      "rel" : "terms-of-service",
      "type" : "text/html",
      "href" : "https://www.arin.net/resources/registry/whois/tou/"
    } ]
  }, {
    "title" : "Whois Inaccuracy Reporting",
    "description" : [ "If you see inaccuracies in the results, please visit: " ],
    "links" : [ {
      "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
      "rel" : "inaccuracy-report",
      "type" : "text/html",
      "href" : "https://www.arin.net/resources/registry/whois/inaccuracy_reporting/"
    } ]
  }, {
    "title" : "Copyright Notice",
    "description" : [ "Copyright 1997-2024, American Registry for Internet Numbers, Ltd." ]
  } ],
  "handle" : "NET-149-43-0-0-1",
  "startAddress" : "149.43.0.0",
  "endAddress" : "149.43.255.255",
  "ipVersion" : "v4",
  "name" : "COLGATE-1",
  "type" : "DIRECT ALLOCATION",
  "parentHandle" : "NET-149-0-0-0-0",
  "events" : [ {
    "eventAction" : "last changed",
    "eventDate" : "2023-08-15T20:06:24-04:00"
  }, {
    "eventAction" : "registration",
    "eventDate" : "1997-07-08T00:00:00-04:00"
  } ],
  "links" : [ {
    "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
    "rel" : "self",
    "type" : "application/rdap+json",
    "href" : "https://rdap.arin.net/registry/ip/149.43.0.0"
  }, {
    "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
    "rel" : "alternate",
    "type" : "application/xml",
    "href" : "https://whois.arin.net/rest/net/NET-149-43-0-0-1"
  } ],
  "entities" : [ {
    "handle" : "COLGAT-2-Z",
    "vcardArray" : [ "vcard", [ [ "version", { }, "text", "4.0" ], [ "fn", { }, "text", "Colgate University" ], [ "adr", {
      "label" : "13 Oak Drive\nHamilton\nNY\n13346\nUnited States"
    }, "text", [ "", "", "", "", "", "", "" ] ], [ "kind", { }, "text", "org" ] ] ],
    "roles" : [ "registrant" ],
    "links" : [ {
      "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
      "rel" : "self",
      "type" : "application/rdap+json",
      "href" : "https://rdap.arin.net/registry/entity/COLGAT-2-Z"
    }, {
      "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
      "rel" : "alternate",
      "type" : "application/xml",
      "href" : "https://whois.arin.net/rest/org/COLGAT-2-Z"
    } ],
    "events" : [ {
      "eventAction" : "last changed",
      "eventDate" : "2023-08-06T11:42:24-04:00"
    }, {
      "eventAction" : "registration",
      "eventDate" : "2023-08-06T11:42:24-04:00"
    } ],
    "entities" : [ {
      "handle" : "NSOCO1-ARIN",
      "vcardArray" : [ "vcard", [ [ "version", { }, "text", "4.0" ], [ "adr", {
        "label" : "13 Oak Drive\nHamilton\nNY\n13346\nUnited States"
      }, "text", [ "", "", "", "", "", "", "" ] ], [ "fn", { }, "text", "Colgate NSO" ], [ "n", { }, "text", [ "NSO", "Colgate", "", "", "" ] ], [ "kind", { }, "text", "individual" ], [ "email", { }, "text", "dnsadmin@colgate.edu" ], [ "tel", {
        "type" : [ "work", "voice" ]
      }, "text", "+1-315-228-7924" ], [ "tel", {
        "type" : [ "work", "cell" ]
      }, "text", "+1-315-228-7111" ] ] ],
      "roles" : [ "administrative" ],
      "links" : [ {
        "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
        "rel" : "self",
        "type" : "application/rdap+json",
        "href" : "https://rdap.arin.net/registry/entity/NSOCO1-ARIN"
      }, {
        "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
        "rel" : "alternate",
        "type" : "application/xml",
        "href" : "https://whois.arin.net/rest/poc/NSOCO1-ARIN"
      } ],
      "events" : [ {
        "eventAction" : "last changed",
        "eventDate" : "2022-12-14T08:53:31-05:00"
      }, {
        "eventAction" : "registration",
        "eventDate" : "2009-11-03T16:04:52-05:00"
      } ],
      "status" : [ "validated" ],
      "port43" : "whois.arin.net",
      "objectClassName" : "entity"
    }, {
      "handle" : "NSO26-ARIN",
      "vcardArray" : [ "vcard", [ [ "version", { }, "text", "4.0" ], [ "adr", {
        "label" : "13 Oak Drive\nHamilton\nNY\n13346\nUnited States"
      }, "text", [ "", "", "", "", "", "", "" ] ], [ "fn", { }, "text", "Network Systems and Operations" ], [ "org", { }, "text", "Network Systems and Operations" ], [ "kind", { }, "text", "group" ], [ "email", { }, "text", "nso@colgate.edu" ], [ "tel", {
        "type" : [ "work", "voice" ]
      }, "text", "+1-315-228-7924" ], [ "tel", {
        "type" : [ "work", "cell" ]
      }, "text", "+1-315-228-7485" ] ] ],
      "roles" : [ "technical", "noc", "abuse" ],
      "links" : [ {
        "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
        "rel" : "self",
        "type" : "application/rdap+json",
        "href" : "https://rdap.arin.net/registry/entity/NSO26-ARIN"
      }, {
        "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
        "rel" : "alternate",
        "type" : "application/xml",
        "href" : "https://whois.arin.net/rest/poc/NSO26-ARIN"
      } ],
      "events" : [ {
        "eventAction" : "last changed",
        "eventDate" : "2023-07-19T11:04:25-04:00"
      }, {
        "eventAction" : "registration",
        "eventDate" : "2009-11-03T15:40:30-05:00"
      } ],
      "status" : [ "validated" ],
      "port43" : "whois.arin.net",
      "objectClassName" : "entity"
    } ],
    "port43" : "whois.arin.net",
    "objectClassName" : "entity"
  }, {
    "handle" : "RG3622-ARIN",
    "vcardArray" : [ "vcard", [ [ "version", { }, "text", "4.0" ], [ "adr", {
      "label" : "13 Oak Drive\nHamilton\nNY\n13346\nUnited States"
    }, "text", [ "", "", "", "", "", "", "" ] ], [ "fn", { }, "text", "DNSADMIN" ], [ "org", { }, "text", "DNSADMIN" ], [ "kind", { }, "text", "group" ], [ "email", { }, "text", "dnsadmin@colgate.edu" ], [ "tel", {
      "type" : [ "work", "voice" ]
    }, "text", "+1-315-228-7924" ], [ "tel", {
      "type" : [ "work", "cell" ]
    }, "text", "+1-315-228-7485" ] ] ],
    "roles" : [ "technical" ],
    "links" : [ {
      "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
      "rel" : "self",
      "type" : "application/rdap+json",
      "href" : "https://rdap.arin.net/registry/entity/RG3622-ARIN"
    }, {
      "value" : "https://rdap.arin.net/registry/ip/149.43.80.3",
      "rel" : "alternate",
      "type" : "application/xml",
      "href" : "https://whois.arin.net/rest/poc/RG3622-ARIN"
    } ],
    "events" : [ {
      "eventAction" : "last changed",
      "eventDate" : "2023-07-19T11:04:48-04:00"
    }, {
      "eventAction" : "registration",
      "eventDate" : "1997-07-08T11:14:35-04:00"
    } ],
    "status" : [ "validated" ],
    "port43" : "whois.arin.net",
    "objectClassName" : "entity"
  } ],
  "port43" : "whois.arin.net",
  "status" : [ "active" ],
  "objectClassName" : "ip network",
  "cidr0_cidrs" : [ {
    "v4prefix" : "149.43.0.0",
    "length" : 16
  } ],
  "arin_originas0_originautnums" : [ ]
}
```
The `get_ASes` function should **return a list of names extracted from the entities section of the JSON responses**: e.g., `['Colgate University', 'NYSERNet', 'Google LLC']`. You should only look at the first entity, and only include the entity if its role is "registrant." If an IP address is in the range of [private addresses defined in RFC 1918](https://datatracker.ietf.org/doc/html/rfc1918#section-3), then skip this address. If a sequence of routers have IPs from the same registrant, the registrant should only be included once.

For example, when you run `path.py` with `traceroute_data/google.txt`, the program should output:

```
ASes (3)
        Colgate University
        NYSERNet
        Google LLC
```

## Part 3: Analyzing network paths

Your last task is to use your traceroute output from [Part 1](#part-1-tracing-paths) and your completed Python program from [Part 2](#part-2-autonomous-system-as-path) to answer the Part 3 questions in `questions.md`.

Note that router hostnames often contain identifiers (e.g., airport codes, city or state abbreviations, etc.) that indicate a router’s approximate geographic location.  For example, consider the hostnames of the routers in the path from your Docker container to Google:
```
vlan0080-hsrp-1.colgate.edu
edge-router-case-bgp.colgate.edu
alb-9204-colgate-cdn.nysernet.net
nyc-9208-alb-9204-cdn.nysernet.net
nyc32-55a1-nyc32-9208-cdn.nysernet.net
lga34s35-in-f14.1e100.net
```
The keywords `alb` and `nyc` correspond to the cities Albany, NY and New York, NY. The keyword `lga` is the airport code for LaGuardia Airport in New York City.

🛑  **Answer the Part 3 questions in `questions.md`**

## Submission instructions

When you are done, you should commit and push your changes to `path.py` and `questions.md` to GitHub.
