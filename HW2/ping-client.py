#Vanshika Shah
#UCID: vns25
#Section 003

#! /usr/bin/env python3
# Echo Client
import sys
import socket
import struct 
import time

# Retrieve host + port from command line arguments 
host = sys.argv[1]
port = int(sys.argv[2])

print("Pinging " + str(host) + ", " + str(port) + ":")

# Socket Connection 
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Timeout 
clientsocket.settimeout(1)

RTT = [] 
received = 0
# 10 Ping Requests 
for seqNum in range(1,11): 

    # Send network-byte-order message to server 
    data = struct.pack('hh', 1, seqNum) # https://docs.python.org/3/library/struct.html 
    start = time.time() 
    clientsocket.sendto(data,(host, port))

    #If server responds, print out RTT, else print message timed out 
    try:
      dataEcho, address = clientsocket.recvfrom(1024)
      total = time.time() - start
      RTT.append(total)
      received = received + 1
      print( "Ping message number " + str(seqNum) + " RTT: " + str(total) + " secs" )

    except Exception: 
      print("Ping message number " + str(seqNum) + " timed out")

#Statistics #https://stackoverflow.com/questions/55193968/minimum-and-maximum-sums-from-a-list-python
loss =   int( ( 1.0 - (received / seqNum) ) * 100 )
minTime = min(RTT)
maxTime = max(RTT)
avg =  sum(RTT) / seqNum 

print( str(seqNum) + " packets transmitted, " + str(received) + " received, "  + str(loss) + "% packet loss" )
print( "Min/Max/Av RTT = " + str(minTime) + " / " + str(maxTime) + " / " + str(avg) + " secs" )

#Close the client socket
clientsocket.close()
