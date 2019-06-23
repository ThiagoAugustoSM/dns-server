# DNS SERVER

import socket
import _thread as t

# AF_INET = Intenet Address Family
# SOCK_STREAM = TCP

class DNSServer:

  def __init__(self, IP_ADDR, PORT, initTable):
    self.IP_ADDR = IP_ADDR
    self.PORT = PORT
    self.tableOfDomains = initTable

  def handleRequest(self, data):
    content = data.decode().split('/')
    
    print(content[0])
    print(content[1])
    print(content[2])
    # Request made by the client
    # Return the IP Address
    if content[0] == 'GET':
      if content[1] in self.tableOfDomains:
        return self.tableOfDomains[content[1]]
      else:
        return 'NOT FOUND'
    # Request made by the server
    elif content[0] == 'POST':
      if content[1] in self.tableOfDomains:
        self.tableOfDomains[content[1]] = content[2]
        print('Domain Updated: ', content[1], ' -> ', content[2])
        return 'DOMAIN UPDATED'
      else:
        self.tableOfDomains[content[1]] = content[2]
        print('Domain Created: ', content[1], ' -> ', content[2])
        return 'DOMAIN CREATED'
    else:
      return '404'

  def onNewClient(self, conn, addr):
    with conn:
        print('Connected by: ', addr)
        while True:
          data = conn.recv(1024)
          print(data.decode())

          response = self.handleRequest(data)
          response = response.encode()
          conn.sendall(response)
          break
          # if conn.recv b'' then we close the connection
          if not data:
            break
          conn.sendall(data)

  def openConnection(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.IP_ADDR, self.PORT))
      s.listen()
      print("DNS Server Started")
      while True:

        # Listening to multiple connections
        conn, addr = s.accept()
        t.start_new_thread(self.onNewClient(conn, addr))

def main():

  DNS_IP = '127.0.0.1'
  DNS_PORT = 53

  initTable = {'host.com': '127.0.0.1'}
  dns = DNSServer(DNS_IP, DNS_PORT, initTable)
  dns.openConnection()

main()