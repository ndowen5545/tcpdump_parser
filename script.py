#!/usr/bin/env python
from IPy import IP
import getpass, time

current_user = getpass.getuser()
tcpinput = ['/home/' + current_user + '/packets-master/', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', '/tmp/tcpoutput.pcap']
#                              sdir                       specip   sip     dip    specpt  sport   dport           dfile

banner = "\n\n\n          ~~~~~~~~~~~~~~~~~~~~ TCPDUMP PARCER ~~~~~~~~~~~~~~~~~~~~"
def menu_text():
  print "This script is designed to allow tcpdump to parce through multiple PCAP files as well as simplify the tcpdump command.\n"
  
  print "If you do not want to search for a certain field, leave empty."
  print "There is no need to input any data for non-essential fields."
  print "By default, the source file path is the 'packets-master/' directory within the current user's home directory."
  print "By default, the destination file is 'tcpoutput.pcap' in the '/tmp/' directory."
  
  print"              --------------Current configuration-------------"
  print " Source File Path: ", tcpinput[0]
  print "  Dest. File Path: ", tcpinput[7], "\n"
  for i in range(len(tcpinput)):
    if not tcpinput[i] == 'NULL':
      if i == 1:
        
        print "    Specific IP/Network: ", tcpinput[1]
      elif not i == 1:
        if i == 2:
          print "      Source IP/Network: ", tcpinput[2]
        if i == 3:
          print " Destination IP/Network: ", tcpinput[3]
      if i == 4:
        
        print "\n    Specific Port/Range: ", tcpinput[4]
      elif not i == 4:
        if i == 5:
          print "\n      Source Port/Range: ", tcpinput[5]
        if i == 6:
          print " Destination Port/Range: ", tcpinput[6]
  print "              ------------------------------------------------"

  print "If a specific IP or port is made, source/destination IPs/ports will be nulled."

  print "NOTE: Put 'C' infront of the option you want to NULL out."
  print "          (Reverts directories back to default)"

  print "Please choose from the following options:"
  print "        1) Specific IP/Network              4) Specific Port/Range"
  print "        2) Source IP/Network                5) Source Port/Range"
  print "        3) Destination IP/Network           6) Destination Port/Range\n"
    
  print "        7) Source File                      8) Destination File\n"
    
  print "        E) Execute tcpdump with current configuration"
  print "        Q) Quit script"

def ip_func(s):
    while True:
      print "\nIf at anytime you want to leave, just enter 'M'\n\nCIDR and subnet mask are indicated with '/'.\nRange is indicated with first IP and second IP being seperated with '-'\n\nPlease put a valid IP address or IP range."
      if s == "1":
        user = raw_input("Specific IP/Network = ")
      elif s == "2":
        user = raw_input("Source IP/Network = ")
      elif s == "3":
        user = raw_input("Destination IP/Network = ")
      if user.lower() == "m":
        break
      elif validate_ip(user) is False:
        print "\nERROR: INVALID INPUT\nPlease input a valid IP address, network range, or subnet/CIDR.\n\n"
      elif validate_ip(user) is True:
        if list(user).count("/") == 1 or list(user).count("-") == 1:
          tcpinput[int(s)] = IP(user, make_net=True)
        else:
          tcpinput[int(s)] = user
        if s == "1":  
          tcpinput[2] = tcpinput[3] = 'NULL'
        elif s == "2" or "3":
          tcpinput[1] = 'NULL'
        break
      else:
        print "\nERROR: INVALID INPUT\nPlease input a valid IP address, network range, or subnet/CIDR.\n\n"
def validate_ip(ip_addr):
  try:
    if IP(ip_addr):
      return True
  except:
    if IP(ip_addr, make_net=True):
      return True


def port_func(s):
  while True:
      print "\nIf at anytime you want to leave, just enter 'M'\n\nPlease input a valid port number."
      if s == "4":
        user = raw_input("Specific Port = ")
      elif s == "5":
        user = raw_input("Source Port = ")
      elif s == "6":
        user = raw_input("Destination Port = ")
      if user.lower() == "m":
        break
      elif validate_port(user) is False:
        print "\nERROR: INVALID INPUT\nPlease input a valid port number.\n\n"
      elif validate_port(user) is True:
        if s == "4":
          tcpinput[4] = user
          tcpinput[5] = tcpinput[6] = 'NULL'
        elif s == "5":
          tcpinput[5] = user
          tcpinput[4] = 'NULL'
        elif s == "6":
          tcpinput[6] = user
          tcpinput[4] = 'NULL'
        break
      else:
        print "\nERROR: INVALID INPUT\nPlease input a valid Port number.\n\n"
def validate_port(port):
  if not port.isdigit():
      return False
  elif int(port) < 0 or int(port) > 65535:
    return False
  else:
    return True

def main():
  while True:
    print banner
    menu_text()
    user = raw_input(">>>")
    if len(user) > 2:
      print "\nERROR: INVALID INPUT\nPlease input a valid option."
    elif list(user)[0] in ["1", "2", "3"]: # IP options
      if len(user) == 2:
        if list(user)[1].lower() == "c": # Clear specified IP option
          tcpinput[int(list(user)[0])] = 'NULL'
      else:  
        ip_func(user)
    elif list(user)[0] in ["4", "5", "6"]: # Port options
      if len(user) == 2:
        if list(user)[1].lower() == "c": # Clear specified port option
          tcpinput[int(list(user)[0])] = 'NULL'
      else:  
        port_func(user)
      
    #elif user == "7":
      
      
    elif user.lower() == "e":
      tcpd_com = "for i in `find " + str(tcpinput[0]) + " -type f` ; do tcpdump -n -r $i" 
      for i in range(len(tcpinput)): # Checks each entry in tcpinput
        if not (i == 0 or i == 7) and not tcpinput[i] == 'NULL': # Skips NULL data
          if i == 2:
              tcpd_com += " src"
          if i == 3:
            tcpd_com += " dst"
          if not (i == 0 or i == 7) and list(str(IP(tcpinput[i], make_net=True))).count("/") == 1: # Network entry checker
            tcpd_com += " net " + str(tcpinput[i])
          elif i in range(1, 4):
            tcpd_com += " host " + str(tcpinput[i])

          if i == 4:
            tcpd_com += " port " + str(tcpinput[4])
          elif not i == 2:
            if i == 5:
              tcpd_com += " src port " + str(tcpinput[5])
            if i == 6:
              tcpd_com += " dst port " + str(tcpinput[6])
      tcpd_com += " -w /tmp/$i'.tmpdump'; done && mergecap  -w " + str(tcpinput[7]) + " /tmp/*.tmpdump && find -type f -name /tmp/'*tmpdump*' -delete"
      print tcpd_com
    elif user.lower() == "q":
      break
    else:
      print "\nERROR: INVALID INPUT\nPlease input a valid option."
main()
