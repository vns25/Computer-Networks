#Vanshika Shah

#! /usr/bin/env python3
# Echo Server
import sys
import socket
import struct
import random 

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages

while True:
  rand = random.randint(0,10) #https://www.programiz.com/python-programming/examples/random-number

  # Receive data from client
  data, address = serverSocket.recvfrom(1024)
  seqNum = struct.unpack('hh', data)[1]
  response = struct.pack('hh', 2, seqNum) 

  #Server responds if random < 4
  if rand >= 4: 
    print("Responding to ping request with sequence number: " + str(seqNum) )
    serverSocket.sendto(response, address)

  else: 
    print("Message with sequence number " + str(seqNum) + " dropped")
