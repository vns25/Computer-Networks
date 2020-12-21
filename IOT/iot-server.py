#! /usr/bin/env python3
# Echo Server
import sys
import socket
import struct
import random 

colors_lst = ['white', 'green', 'blue', 'red', 'yellow', 'white', 'black', 'aqua', 'purple' ]

class Bulb: 
    color = "none"
    status = "OFF"
        
    def get_bulb_pow(self):
        return self.status 

    def get_color(self): 
        return self.color 
    
    def set_color(self, color2): 
        self.color = color2
    
    def set_status(self, status2): 
        self.status = status2
        
# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

bulb = Bulb() 
# loop forever listening for incoming UDP messages
while True:
  # Receive data from client
  data, address = serverSocket.recvfrom(1024)
  color_len = struct.unpack_from('!hhihhh', data)[3]
  mes_id = struct.unpack('!hhihhh', data[:14])[2] 
  power_req = struct.unpack('!hhihhh' + str(color_len) + 's', data)[5]
  color_req = struct.unpack('!hhihhh' + str(color_len) + 's', data)[6].decode() 
  
  answer = "" 
  color = "none"
  bulb_power = 0
  return_code = 0

  # turn bulb on 
  if power_req == 1: 
    # turn bulb on 
    if color_req == "none": 
        bulb.set_color("white")
        bulb.set_status("ON")
        color = "white"
        answer = "Bulb No. 1 is ON and set to white" 
    # turn bulb on and set color 
    elif color_req in colors_lst: 
        bulb.set_status("ON")
        bulb.set_color(color_req)
        color = color_req
        answer = "Bulb 1 is ON and set to " + color_req 
    bulb_power = 1
    
  # turn bulb off 
  elif color_req == "none" and power_req == 0: 
      bulb.set_status("OFF")
      answer = "Bulb 1 has been turned OFF"

  # get status 
  elif power_req == 2 and color_req == "none": 
    color = bulb.get_color()
    if bulb.get_bulb_pow() == "ON": 
      bulb_power = 1
    answer = "Bulb 1 is " + bulb.get_bulb_pow() + " and color is " + bulb.get_color() 

  # set color 
  elif power_req == 3: 
      if color_req not in colors_lst and color_req != "none": 
        bulb_power = 2
        return_code = 2
        color = "error"
        answer = "Color not supported at the moment"
      elif bulb.get_bulb_pow() != "OFF": 
        bulb.set_color( color_req )
        bulb_power = 1
        answer = "Bulb 1 is " + bulb.get_bulb_pow() + " and color is " + bulb.get_color() 
      else: 
        color = "error"
        return_code = 3
        answer = "Please turn on the bulb before changing color"

  # incorrect message format 
  else: 
    return_code = 1
    bulb_power = 2
    color = "error"
    answer = "Unknown command"
    
  color_len = len(color)
  answer_len = len(answer)

  # Send application data to client 
  response = struct.pack('!hhihhh' + str(color_len) + 's' + str(answer_len) + 's', 2, return_code, mes_id, color_len, answer_len, bulb_power, str.encode( color ), str.encode( answer ) ) 
  serverSocket.sendto( response, address ) 

  
  

