#Vanshika Shah
#UCID: vns25
#Section 003

#! /usr/bin/env python3
# Echo Server
import sys
import socket
import codecs 
import datetime, time 
from datetime import timezone
import os

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int( sys.argv[2] )
dataLen = 1000000

# Create a TCP welcoming socket 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assign server IP address and port number to socket
serverSocket.bind( (serverIP, serverPort) )

#Listen for incoming connection requests 
serverSocket.listen(1)

print('The server is ready to receive on port: ' + str(serverPort) + '\n')

# loop forever listening for incoming connection requets 
while True:
    connectionSocket, address = serverSocket.accept()

    # Receive GET request and ignore headers 
    data = ""
    if_mod_time = ""
    headers_recv = connectionSocket.recv(dataLen).decode().splitlines() 
    for header in headers_recv: 
        if "GET" in header: 
            filename = header.split()[1][1:]
            data = data + header + "\r\n"
        elif "Host" in header: 
            data = data + header + "\r\n" 
        elif "If-Modified-Since" in header: 
            if_mod_time = header[19:] + "\r\n"
            data = data + header + "\r\n" 
    data = data + "\r\n"

    # get current time in UTC and convert to string in HTTP format 
    t = datetime.datetime.utcnow() 
    date = t.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n")   

    status1 = "HTTP/1.1 200 OK\r\n" 
    status2 = "HTTP/1.1 304 Not Modified\r\n"
    status3 = "HTTP/1.1 404 Not Found\r\n"

    # check if file exists https://careerkarma.com/blog/python-check-if-file-exists/#:~:text=To%20check%20if%2C%20in%20Python,exists()%20checks%20for%20both.
    if not os.path.isfile(filename): 
        response = status3 + "Date: " + date + "Content-Length: " + "0\r\n" + "\r\n"
    else: 
        # determine file's modification time 
        secs = os.path.getmtime( filename )
        t = time.gmtime( secs ) 
        last_mod_time = time.strftime( "%a, %d %b %Y %H:%M:%S GMT\r\n", t )

        #get body 
        file = codecs.open(filename, "r", "utf-8") # https://www.kite.com/python/answers/how-to-open-an-html-file-in-python#:~:text=Use%20codecs.,file%20in%20read%2Donly%20mode.
        body = file.read() 

        #get content length https://stackoverflow.com/questions/6591931/getting-file-size-in-python and content type
        content_len = str ( os.path.getsize(filename) ) + "\r\n"
        content_type = "text/html; charset=UTF-8\r\n"

        #conditional GET 
        if if_mod_time != "": 
            # if not modified on server 
            if if_mod_time == last_mod_time: 
                response = status2 + "Date: " + date + "\r\n"
            else: 
                response = status1 + "Date: " + date + "Last-Modified: " + last_mod_time + "Content-Length: " + content_len + "Content-Type: " + content_type + "\r\n" + body
        else: 
            response = status1 + "Date: " + date + "Last-Modified: " + last_mod_time + "Content-Length: " + content_len + "Content-Type: " + content_type + "\r\n" + body
    
    # Echo back to client
    connectionSocket.send( response.encode() )
    connectionSocket.close()


  

