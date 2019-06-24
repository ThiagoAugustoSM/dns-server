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
    socket.send(content.encode())
    
    #Answer about the size
    size = socket.recv(1024)
    size = int(size.decode())
    
    socket.sendall(b'Ok!')

    print('\nRecebendo o arquivo...')
    fileSize = 0
    
    with open(fileName, 'wb') as f:
      while True:
        data = socket.recv(1024)
        f.write(data)
        fileSize += len(data)
        if(fileSize >= size): break
    print('Arquivo salvo!\n')
  
  def solicitarLista(self, socket):
    content = 'GET/list'
    socket.send(content.encode())

    response = socket.recv(1024).decode()
    response = response.split('/')
    print('Os arquivos contidos no servido sao:')
    for r in response:
      print('- ', r)
    print('')

def responseParser(data):
  return data.decode()

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