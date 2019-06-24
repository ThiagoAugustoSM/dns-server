# Client 

import sys
sys.path.append('../')
import socket
import os
from Constants.constants import DNS_IP, DNS_PORT, SERVER_PORT, SERVER_DOMAIN

class Client:

  def __init__(self, SERVER_DOMAIN, SERVER_PORT, DNS_IP, DNS_PORT):
    self.SERVER_DOMAIN = SERVER_DOMAIN
    self.SERVER_IP = ''
    self.SERVER_PORT = SERVER_PORT
    self.DNS_IP = DNS_IP
    self.DNS_PORT = DNS_PORT

  def connectDNS(self):

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      content = 'GET/' + self.SERVER_DOMAIN
      s.sendto(content.encode(), (self.DNS_IP, self.DNS_PORT))
      data = s.recv(1024)
      IP = data.decode()
      return IP
    print('Received', data)

  def connectServer(self):

    print('Connecting to server...')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      print('Connected to: ', self.SERVER_DOMAIN, '\n')      
      while True:
        choice, fileName = self.userChoice()
        
        if choice == '1':
          self.solicitarArquivo(fileName, s)
        elif choice == '2':
          self.solicitarLista(s)
        elif choice == '3':
          break
    #print('Received', data)

  def userChoice(self):
    print('Qual acao voce deseja tomar?\n')
    print('1 - Solicitar um arquivo do servidor')
    print('2 - Lista dos arquivos disponiveis do servidor')
    print('3 - Encerrar a conexao')
    choice = input('\n:')
    
    fileName = ''
    if(choice == '1'):
      fileName = input('\nQual o nome do arquivo?: ')
    
    return choice, fileName

  def setServerIP(self, serverIP):
    self.SERVER_IP = serverIP

  def solicitarArquivo(self, fileName, socket):
    content = 'GET/file/' + fileName
    socket.sendto(content.encode(), (self.SERVER_IP, self.SERVER_PORT))
    
    #Answer about the size
    size, client = socket.recvfrom(1024)
    size = int(size.decode())
    socket.sendto(b'Ok!', client)
    print('Size:', size)

    print('\nRecebendo o arquivo...')
    fileSize = 0
    
    package = {}
    with open(fileName, 'wb') as f:
      while True:
        # Receiving the next package
        data, server = socket.recvfrom(1024)
        # ACK about the last package
        socket.sendto(data[-16:0], server)
        
        # Add the tuple Index:Data to the package Dict
        package[data[-16:]] = data[0:-16]
        fileSize += len(data[0:-16])
        if(fileSize >= size): break
    
      for i in sorted(package):
        f.write(package[i])

    print('Arquivo salvo!\n')
  
  def solicitarLista(self, socket):
    content = 'GET/list'
    socket.sendto(content.encode(), (self.SERVER_IP, self.SERVER_PORT))

    response, client = socket.recvfrom(1024)
    response = response.decode().split('/')
    print('Os arquivos contidos no servido sao:')
    for r in response:
      print('- ', r)
    print('')

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