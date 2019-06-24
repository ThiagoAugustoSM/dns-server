# dns-server

This project is a minimal implementation of a DNS server in Python 3.

It is also the final project of the discipline Communication Infrastructure at UFPE.

## Ideia

The ideia is that the Client requests the real IP Address of the Server, that is contained in a table of the DNS Server, that was previously updated by the server itself. And after that a connection is started between the Client and Server, with the purpose of providing a shell terminal and some services regarding files contained in Server directory.  

## How to run

- In three terminal separated, in order, run:
  - cd DNS && python dns.py
  - cd Server && python server.py
  - cd Client && python client.py

After that the Client will be provided by a shell with some services 

You can change the content and files existing in _Server/files_ folder, to be used by the Client.


## If you are running on **Linux**

The common port to use on DNS Servers is 53, but you can have some programs already using it, so you can do two things:
- Change the port of the DNS Server in _constants.py_ or
- Kill the program that is using the port 53 with the following terminal line (not recommended): 
`kill $(lsof -t -i:8080)`

The same thing can be done to the Server's Port.

## Constants file

The constants file contains the definitions for the commonm IP, PORT and Domains shared with the Client, Server and DNS Server.

## Types of Messages

| From -> To        | Format           | Response  | Objective
| ------------- |:-------------:| -----:| -------:|
| Client -> DNS | GET/{SERVER_DOMAIN} | {SERVER_IP} |   Get the IP Address from a Server Domain      |
| Server -> DNS | POST/{SERVER_DOMAIN}/{SERVER_IP}      |  'UPDATE IN TABLE' OR NOT | Update or create a relation of a Server Domain and IP in the DNS Table |
| Client -> Server | GET/file/{FILE_NAME}      |  FILE | Downloading a file existing from the Server|
| Client -> Server | GET/list      |  LIST OF FILE NAMES | Get the list of existing files in the Server|