# dns-server

This project is a minimal implementation of a DNS server in Python 3.

It is also the final project of the discipline Communication Infrastructure at UFPE.

## If you are running on **Linux**

The common port to use on DNS Servers is 53, but you can have some programs already using it, so you can do two things:
- Change the port of the DNS Server in _constants.py_ or
- Kill the program that is using the port 53 with the following terminal line (not recommended): 
`kill $(lsof -t -i:8080)`

The same thing can be done to the Server's Port.

## Types of Messages

| From -> To        | Format           | Response  | Objective
| ------------- |:-------------:| -----:| -------:|
| Client -> DNS | GET/{SERVER_DOMAIN} | {SERVER_IP} |   Get the IP Address from a Server Domain      |
| Server -> DNS | POST/{SERVER_DOMAIN}/{SERVER_IP}      |  'UPDATE IN TABLE' OR NOT | Update or create a relation of a Server Domain and IP in the DNS Table |
| Client -> Server | GET/file/{FILE_NAME}      |  FILE | Downloading a file existing from the Server|
| Client -> Server | GET/list      |  LIST OF FILE NAMES | Get the list of existing files in the Server|