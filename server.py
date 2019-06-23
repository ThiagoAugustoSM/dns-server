# SERVER

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 80        # Port to listen on (non-privileged ports are > 1023)

DOMAIN = 'server.com'
DNS_IP = '127.0.0.1'
DNS_PORT = 53


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

connectDNS(DOMAIN, DNS_IP, DNS_PORT)
createServer(HOST, PORT)
