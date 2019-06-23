# DNS SERVER

import socket

# AF_INET = Intenet Address Family
# SOCK_STREAM = TCP

class DNSServer:

  def __init__(self, IP_ADDR, PORT, initTable):
    self.IP_ADDR = IP_ADDR
    self.PORT = PORT
    self.tableOfDomains = initTable

  def handleRequest(self, data):
    content = data.decode().split('/')
    if content[0] == 'GET':
      if content[1] in self.tableOfDomains:
        return self.tableOfDomains[content[1]]
      else:
        return 'NOT FOUND'
    elif content[0] == 'POST':
      self.tableOfDomains[content[1]] = content[2]

  def openConnection(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.IP_ADDR, self.PORT))
      s.listen()
      conn, addr = s.accept()

      with conn:
        print('Connected by: ', addr)
        while True:
          data = conn.recv(1024)
          print(data.decode())
          IP = self.handleRequest(data)
          response = IP.encode()
          conn.sendall(response)
          break
          # if conn.recv b'' then we close the connection
          if not data:
            break
          conn.sendall(data)

def main():

  initTable = {'host.com': '127.0.0.1'}
  dns = DNSServer('127.0.0.1', 53, initTable)
  dns.openConnection()

main()