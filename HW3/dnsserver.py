#Vanshika Shah
#UCID: vns25
#Section 003

#! /usr/bin/env python3
# Echo Server
import sys
import socket
import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

# loop forever listening for incoming UDP messages
while True:
  # Open file 
  dnsFile = open('dns-master.txt') #http://www.compciv.org/guides/python/fileio/open-and-read-text-files/

  # Receive data from client
  data, address = serverSocket.recvfrom(1024)
  questionLen = struct.unpack_from('!hhihh', data)[3]
  question = struct.unpack('!hhihh' + str(questionLen) + 's', data)[5].decode() 
  mesId = struct.unpack('!hhihh' + str(questionLen) + 's', data)[2] 

  answer = "" 
  returnCode = 1
  lst=[]

  # Append resource records in a list 
  for line in dnsFile: 
    lst.append(line[:-1])
  
  # Find answer in the list 
  for resRecord in lst: 
    if question in resRecord: 
      answer = resRecord
      returnCode = 0

  answerLen = len(answer)

  # Send application data to client 
  response = struct.pack('!hhihh' + str(questionLen) + 's' + str(answerLen) + 's', 2, returnCode, mesId, questionLen, answerLen, str.encode(question), str.encode(answer) ) 
  serverSocket.sendto(response, address)
  

