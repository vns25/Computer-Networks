
#! /usr/bin/env python3
import sys
import socket
import time
import struct
import random
# Get the server hostname, port as command line arguments
address = sys.argv[1]
port = int(sys.argv[2])
command = sys.argv[3]

if command == "ON":
    power=1
elif command == "OFF":
    power=0
elif command == "SET":
    power=3
elif command == "STATUS":
    power=2
else: 
    power=4
# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)
messageID = random.randint(0,100)
answerLength=0
returnCode=0

if len(sys.argv) >= 5: 
    question = sys.argv[4]
else: 
    question="none"

questionByte=question.encode()
questionLength=len(str(question))
print("Sending Request to  " + address + ", " + str(port) + ":")
print("Message ID: " + str(messageID))
print("Power: " + str( power) )
print("Color: " + str(question) )
print("Question Length: " + str(questionLength) + " bytes")
print("Answer Length: " + str(answerLength) + " bytes")
network=("!hhihhh" + str(questionLength)+"s")
data = struct.pack("!hhihhh" + str(questionLength)+"s", 1, returnCode, messageID, questionLength, answerLength, power, questionByte)

for i in range(3):
    try:
        clientsocket.sendto( data,(address, port) )
        dataEcho, address = clientsocket.recvfrom(1024)
        
        serverInfo = struct.unpack('!hhihhh', dataEcho[:14] )
        returnCode=serverInfo[1]
        messageID=serverInfo[2]
        questionLength=serverInfo[3]
        answerLength=serverInfo[4]
        power=serverInfo[5]
        network=("!hhihhh" + str(questionLength)+"s" + str(answerLength)+"s")
        answerInfo = struct.unpack(network, dataEcho)
        question=answerInfo[6].decode()
        answer=answerInfo[7].decode()
        print("\n")
        if(returnCode==0):
            print("Return Code: 0 (No errors)")
        elif(returnCode==1):
            print("Return Code: 1 (Unsupported Command)")
        elif(returnCode==2):
            print("Return Code: 2 (Unsupported Color)")
        elif(returnCode==4): 
            print("Return Code: 4 (Bulb Broken)")
        else:
            print("Return Code: 3 (change color while OFF)")
        print("Message ID: " + str(messageID))
        print("Bulb No: 1")
        print("Power: " + str(power))
        print("Color: " + str(question))
        print("Question Length: " + str(questionLength) + " bytes")
        print("Answer Length: " + str(answerLength) + " bytes")
        print("Answer: " + str(answer))

        break    
    except: 
        if i==2:
            print("Request timed out … Exiting Program.")
        else:
            print("Request timed out...")
#Close the client socket
clientsocket.close()