# SERVER

import sys
sys.path.append('../')

import socket
from Constants.constants import SERVER_IP, SERVER_PORT, DNS_IP, DNS_PORT, SERVER_DOMAIN
import os


class Server:

  def __init__(self, SERVER_IP, SERVER_PORT, SERVER_DOMAIN, DNS_IP, DNS_PORT):
    self.SERVER_IP = SERVER_IP
    self.SERVER_PORT = SERVER_PORT
    self.SERVER_DOMAIN = SERVER_DOMAIN
    self.DNS_IP = DNS_IP
    self.DNS_PORT = DNS_PORT

  # Connection with DNS Server to setup the domain
  def connectDNS(self):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      content = 'POST/' + self.SERVER_DOMAIN + '/' + self.SERVER_IP
      s.sendto(content.encode(), (self.DNS_IP, self.DNS_PORT))
      data, client = s.recvfrom(1024)
      response = data.decode()
      print(response)
      return response

    print('Received', data)

  def createServer(self):
    print('Server Started at: ', self.SERVER_IP, '::', self.SERVER_PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      s.bind((self.SERVER_IP, self.SERVER_PORT))
      while True:
        data, client = s.recvfrom(1024)
        print('received:', data.decode())
        self.handleRequest(data, client, s)

  def handleRequest(self, data, client, socket):
    request = data.decode().split('/')
    if request[0] == 'GET':
      if request[1] == 'file':
        self.sendFile(request[2], client, socket)
      elif request[1] == 'list':
        self.sendList(client, socket)
      else:
        socket.sendto(b'404', client)
    else:
      socket.sendto(b'404', client) 
    pass

  def fileSize(self, fname):
    return os.stat(fname).st_size

  def sendFile(self, fileName, client, socket):

    fileSize = str(self.fileSize('./files/'+ fileName))
    socket.sendto(fileSize.encode(), client)
    socket.recvfrom(1024)

    # Package will be 1008 + 16 byte(index)
    f = open('./files/'+ fileName, 'rb+')
    l = f.read(1008)
    
    i = 0
    toSend = l + i.to_bytes(16, byteorder="big")
    while(l): # Read until the end of the file
      socket.sendto(toSend, client)
      socket.recvfrom(1024)

      l = f.read(1008)
      i += 1
      #Increment the size in the last part of the package
      toSend = l + i.to_bytes(16, byteorder="big")
    f.close()
    print("Arquivo ", fileName, " enviado com sucesso!")

  def sendList(self, client, socket):

    files = '/'.join(os.listdir('./files')).encode()
    socket.sendto(files, client)

def main():

  server = Server(SERVER_IP, SERVER_PORT, SERVER_DOMAIN,
                  DNS_IP, DNS_PORT)
  server.connectDNS()
  server.createServer()

main()
