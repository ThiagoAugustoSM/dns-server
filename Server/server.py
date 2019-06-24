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

  def responseParser(self, data):
    return data.decode() 

  # Connection with DNS Server to setup the domain
  def connectDNS(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.DNS_IP, self.DNS_PORT))
      content = 'POST/' + self.SERVER_DOMAIN + '/' + self.SERVER_IP
      s.send(content.encode())
      data = s.recv(1024)
      response = self.responseParser(data)
      print(response)
      return response

    print('Received', data)

  def createServer(self):
    print('Server Started at: ', self.SERVER_IP, '::', self.SERVER_PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.SERVER_IP, self.SERVER_PORT))
      s.listen(5)
      conn, addr = s.accept()
      with conn:
        print('Connected by', addr)
        while True:
          data = conn.recv(1024)
          print('received:', data.decode())
          self.handleRequest(data, conn)
          # break
          # if not data:
          #   break
          # conn.sendall(data)

  def handleRequest(self, data, conn):
    request = data.decode().split('/')
    if request[0] == 'GET':
      if request[1] == 'file':
        self.sendFile(request[2], conn)
      elif request[1] == 'list':
        self.sendList(conn)
      else:
        conn.sendall(b'404')
    else:
      conn.sendall(b'404') 
    pass

  def fileSize(self, fname):
    return os.stat(fname).st_size

  def sendFile(self, fileName, conn):

    conn.sendall(str(self.fileSize('./files/'+ fileName)).encode())
    conn.recv(1024)

    f = open('./files/'+ fileName, 'rb+')
    l = f.read(1024)
    while(l):
      conn.send(l)
      l = f.read(1024)
    f.close()
    print("Arquivo ", fileName, " enviado com sucesso!")

  def sendList(self, conn):

    files = '/'.join(os.listdir('./files')).encode()
    conn.sendall(files)

def main():

  server = Server(SERVER_IP, SERVER_PORT, SERVER_DOMAIN,
                  DNS_IP, DNS_PORT)
  server.connectDNS()
  server.createServer()

main()
