# SERVER

import socket
import constants
HOST = constants.SERVER_IP  # Standard loopback interface address (localhost)
PORT = constants.SERVER_PORT        # Port to listen on (non-privileged ports are > 1023)

DNS_IP = constants.DNS_IP
DNS_PORT = constants.DNS_PORT
SERVER_DOMAIN = constants.SERVER_DOMAIN

def responseParser(data):
  return data.decode() 

# Connection with DNS Server to setup the domain
def connectDNS(serverDomain, IP_ADDR, PORT):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDR, PORT))
    content = 'POST/' + serverDomain + '/' + HOST
    s.send(content.encode())
    data = s.recv(1024)
    response = responseParser(data)
    print(response)
    return response

  print('Received', data)

def createServer(HOST, PORT):
  print('Server Started at: ', HOST, '::', PORT)
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
      print('Connected by', addr)
      while True:
        data = conn.recv(1024)
        if not data:
          break
        conn.sendall(data)

connectDNS(SERVER_DOMAIN, DNS_IP, DNS_PORT)
createServer(HOST, PORT)
