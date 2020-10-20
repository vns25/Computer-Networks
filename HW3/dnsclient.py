#Vanshika Shah

#! /usr/bin/env python3
# Echo Client

import sys
import socket
import struct 
import random

# Retrieve ip, port, and hostname from command line args 
ip = sys.argv[1]
port = int(sys.argv[2])
host = sys.argv[3]

print("Sending Request to " + str(ip) + ", " + str(port) + ":")

# Print Message ID, Question Length, Answer Length, & Question 
question = host + ' A IN'
mesId = random.randint(1,100)
questionLen = len(question)

print('Message ID: ' + str(mesId) )
print('Question Length: ' + str(questionLen) + ' bytes' ) 
print('Answer Length: 0 bytes')
print('Question: ' + question + '\n')

# Socket Connection 
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Pack the data into network byte order 
data = struct.pack( '!hhihh' + str(questionLen) + 's', 1, 0, mesId, questionLen, 0, str.encode(question) ) 

# Timeout 
clientsocket.settimeout(1)

# Maximum 3 attempts to send to server 
for i in range(0,3): 
    
    # Sends data to server and prints the server data 
    try:
      clientsocket.sendto( data,(ip, port) )
      dataEcho, address = clientsocket.recvfrom(1024)
      
      s = struct.unpack_from('!hhihh', dataEcho)
      
      returnCode = str(s[1] ) 
      serverMID = str( s[2] ) 
      serverQLen = str( s[3] )
      answerLen = str( s[4] )
      serverQ = struct.unpack_from('!hhihh' + serverQLen + 's' + answerLen + 's', dataEcho)[5].decode() 
      answer = struct.unpack_from('!hhihh' + serverQLen + 's' + answerLen + 's', dataEcho)[6].decode() 

      print('Received Response from ' + str(ip) +  ', ' + str(port) + ':' )

      if returnCode == '0': 
        print('Return Code: ' + returnCode + ' (No errors)' )
      else: 
        print('Return Code: ' + returnCode + ' (Name does not exist)' )
        
      print('Message ID: ' + serverMID ) 
      print('Question Length: ' + serverQLen + ' bytes')
      print('Answer Length: ' + answerLen + ' bytes')
      print('Question: ' + serverQ )

      if returnCode == '0': 
        print('Answer: ' + answer)

      break

    # If server doesn't respond 
    except: 
      if i==2: 
        print("Request timed out... Exiting Program.") 
      else: 
        print("Request timed out... ") 
        print("Sending Request to " + str(ip) + ", " + str(port) + ":")

#Close the client socket
clientsocket.close()
