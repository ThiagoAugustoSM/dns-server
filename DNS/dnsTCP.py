# DNS SERVER

import sys
sys.path.append('../')
import socket
import _thread as t
from Constants.constants import DNS_IP, DNS_PORT

# AF_INET = Intenet Address Family
# SOCK_STREAM = TCP

class DNSServer:

  def __init__(self, IP_ADDR, PORT, initTable):
    self.IP_ADDR = IP_ADDR
    self.PORT = PORT
    self.tableOfDomains = initTable

  def handleRequest(self, data):
    content = data.decode().split('/')

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
        print('\nNew Connection from: ', addr)
        while True:
          data = conn.recv(1024)
          print('Received: ', data.decode())

          response = self.handleRequest(data)
          response = response.encode()
          
          conn.sendall(response)
          print('Connection Closed')
          break
          # if conn.recv b'' then we close the connection
          if not data:
            break
          conn.sendall(data)

  def openConnection(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.IP_ADDR, self.PORT))
      s.listen()
      print("DNS Server Started\n")
      while True:
        # Listening to multiple connections
        conn, addr = s.accept()
        t.start_new_thread(self.onNewClient, (conn, addr))

def main():

  initTable = {'host.com': '127.0.0.1'}
  dns = DNSServer(DNS_IP, DNS_PORT, initTable)
  dns.openConnection()

main()