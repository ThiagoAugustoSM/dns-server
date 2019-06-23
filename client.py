# Client 

import socket
from constants import DNS_IP, DNS_PORT, SERVER_PORT, SERVER_DOMAIN

class Client:

  def __init__(self, SERVER_DOMAIN, SERVER_PORT, DNS_IP, DNS_PORT):
    self.SERVER_DOMAIN = SERVER_DOMAIN
    self.SERVER_IP = ''
    self.SERVER_PORT = SERVER_PORT
    self.DNS_IP = DNS_IP
    self.DNS_PORT = DNS_PORT

  def connectDNS(self):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.DNS_IP, self.DNS_PORT))
      content = 'GET/' + self.SERVER_DOMAIN
      s.send(content.encode())
      data = s.recv(1024)
      IP = data.decode()
      return IP
    print('Received', data)

  def connectServer(self):

    print('Connecting to server...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.SERVER_IP, self.SERVER_PORT))
      print('Connected to: ', self.SERVER_DOMAIN)
      content = 'GET/' + self.SERVER_IP
      s.send(content.encode())
      data = s.recv(1024)
      responseParser(data)
    print('Received', data)

  def setServerIP(self, serverIP):
    self.SERVER_IP = serverIP
def responseParser(data):
  return data.decode() 

def solicitarArquivo():
  pass

def listaArquivos():
  pass
def closeConnection():
  pass

def main():

  print('\nBem Vindo ao DNS Minimal!\n')
  serverDomain = input('Qual dominio voce deseja se conectar? ')
  client = Client(SERVER_DOMAIN, SERVER_PORT, DNS_IP, DNS_PORT)
  IP_ADDR = client.connectDNS()
  if IP_ADDR != 'NOT FOUND':
    client.setServerIP(IP_ADDR)
    client.connectServer()
  else:
    print('Domain not exists in DNS Server.')
main()