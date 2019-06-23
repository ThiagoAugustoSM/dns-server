# Client 

import socket

DNS_IP_ADDR = '127.0.0.1'
DNS_PORT = 53

def connectDNS(serverDomain, IP_ADDR, PORT):

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDR, PORT))
    content = 'GET/' + serverDomain
    s.send(content.encode())
    data = s.recv(1024)
    IP = responseParser(data)
    return IP
  print('Received', data)

def connectServer(IP_SERVER_ADDR, PORT=80):

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_SERVER_ADDR, PORT))
    content = 'GET/' + IP_SERVER_ADDR
    s.send(content.encode())
    data = s.recv(1024)
    responseParser(data)
    print("ME conectei com o server")
  print('Received', data)

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
  IP_ADDR = connectDNS(serverDomain, DNS_IP_ADDR, DNS_PORT)
  connectServer(IP_ADDR)
main()