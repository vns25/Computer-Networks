#Vanshika Shah
#UCID: vns25
#Section 003

#! /usr/bin/env python3
# Echo Client
import sys
import socket
import os

# retrieve hostname, port, and web obj from command line arg
url = sys.argv[1]
ip = url.split(":")[0]
port = int ( url.split(":")[1].split("/")[0] )
filename = url.split(":")[1].split("/")[1] 
file_cached_name = filename.split(".")[0] + "_cache.txt"

# check if file is cached and retrieve last modified time from cached file 
isCached = False 
if os.path.isfile( file_cached_name ): 
    isCached = True
    with open(file_cached_name, "r") as file:
        last_mod_time = file.readline()

# GET request when web object not cached or it doesn't exist 
if not isCached: 
    data = "GET /" + filename + " HTTP/1.1\r\n" + "Host: " + ip + ":" + str(port) + "\r\n" + "\r\n"

# conditional GET request 
else: 
    data = "GET /" + filename +  " HTTP/1.1\r\n" + "Host: " + ip + ":" + str(port) + "\r\n" + "If-Modified-Since: " + last_mod_time + "\r\n"

# socket Connection 
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect( (ip, port) )

# send Request 
clientsocket.send( data.encode() )
print("\n----HTTP Request---- \n\n" + data )

# get request
dataEcho = clientsocket.recv(1024).decode() 

data_lst = dataEcho.splitlines() 
status = data_lst[0]

# cache new files https://www.w3schools.com/python/python_file_write.asp
if status == "HTTP/1.1 200 OK":
    content = ""  
    if isCached: 
        print("File has been modified on server: ")

    # retrieve "Last-Modified time"
    mod_date = data_lst[2][15:]

    for body in data_lst[6:]: 
        content = content + body 

    # cache mod_date and contents 
    cacheFile = open( file_cached_name, "w" ) 
    cacheFile.write( mod_date + "\n" )
    cacheFile.write( content )
    cacheFile.close()

print("----HTTP Response--- \n\n" + dataEcho )
clientsocket.close()
