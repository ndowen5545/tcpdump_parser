#!/usr/bin/env python
from IPy import IP
import getpass, time, os

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
  print "      Source Path: ", tcpinput[0]
  print "  Dest. File Path: ", tcpinput[7], "\n"
  for i in range(len(tcpinput)):
    if not tcpinput[i] == 'NULL':
      if i == 1:
        if "/" in str(tcpinput[1]):
          print "       Specific Network: ", tcpinput[1]
        else:
          print "            Specific IP: ", tcpinput[1]
      elif not i == 1:
        if i == 2:
          if "/" in str(tcpinput[2]):
            print "         Source Network: ", tcpinput[2]
          else:
            print "              Source IP: ", tcpinput[2]
        if i == 3:
          if "/" in str(tcpinput[3]):
            print "    Destination Network: ", tcpinput[3]
          else:
            print "         Destination IP: ", tcpinput[3]
      if i == 4:
        if "-" in str(tcpinput[4]):
          print "\n    Specific Port Range: ", tcpinput[4]
        else:
          print "\n          Specific Port: ", tcpinput[4]
      elif not i == 4:
        if i == 5:
          if "-" in str(tcpinput[5]):
            print "\n      Source Port Range: ", tcpinput[5]
          else:
            print "\n            Source Port: ", tcpinput[5]
        if i == 6 and tcpinput[5] == 'NULL':
          if "-" in str(tcpinput[6]):
            print "\n Destination Port Range: ", tcpinput[6]
          else:
            print "\n       Destination Port: ", tcpinput[6]
        elif i == 6:
          if "-" in str(tcpinput[6]):
            print " Destination Port Range: ", tcpinput[6]
          else:
            print "       Destination Port: ", tcpinput[6]

  print "              ------------------------------------------------"

  print "If a specific IP or port is made, source/destination IPs/ports will be NULL'ed."

  print "NOTE: Put 'C' alone will NULL out all data."
  print "          (Reverts directories back to default)"

  print "Please choose from the following options:"
  print "        1) Specific IP/Network              4) Specific Port/Range"
  print "        2) Source IP/Network                5) Source Port/Range"
  print "        3) Destination IP/Network           6) Destination Port/Range\n"
    
  print "        7) Source Directory                 8) Destination File\n"
  
  print "       #C) Clears a specific entry."  
  print "        E) Execute tcpdump with current configuration"
  print "        Q) Quit script"

def ip_func(s):
    while True:
      print "\nIf at anytime you want to leave, just enter 'M'\n\nCIDR and subnet mask are indicated with '/'.\nRange is indicated with first IP and second IP being seperated with '-'\n\nPlease enter a valid IP address or IP range."
      if s == "1":
        user = raw_input("Specific IP/Network = ")
      elif s == "2":
        user = raw_input("Source IP/Network = ")
      elif s == "3":
        user = raw_input("Destination IP/Network = ")
      if list(user)[0].lower() == "m":
        break
      elif validate_ip(user) is False:
        print "\n\\\\ERROR: INVALID INPUT - Please enter a valid IP addres or network - ERROR: INVALID INPUT//\n\n"
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
        print "\n\\\\ERROR: INVALID INPUT - Please enter a valid IP addres or network - ERROR: INVALID INPUT//\n\n"
def validate_ip(ip_addr):
  try:
    if IP(ip_addr):
      return True
  except:
    if IP(ip_addr, make_net=True):
      return True

def port_func(s):
  while True:
      print "\nIf at anytime you want to leave, just enter 'M'\n\nPort ranges are indicated by entering the first port number, a '-' and a second port number.\nPlease input a valid port number or range."
      if s == "4":
        user = raw_input("Specific Port = ")
      elif s == "5":
        user = raw_input("Source Port = ")
      elif s == "6":
        user = raw_input("Destination Port = ")
      if user.lower() == "m":
        break
      elif validate_port(user) is False:
        print "\n\\\\ERROR: INVALID INPUT - Please enter a valid Port number or range - ERROR: INVALID INPUT//\n\n"
      elif validate_port(user) is True:
        port1 = port2 = 0
        if "-" in user:
          port1, port2 = user.split("-")
        if int(port1) > int(port2):
          if s == "4":
            tcpinput[4] = str(port2) + "-" + str(port1)
            tcpinput[5] = tcpinput[6] = 'NULL'
          elif s == "5":
            tcpinput[5] = str(port2) + "-" + str(port1)
            tcpinput[4] = 'NULL'
          elif s == "6":
            tcpinput[6] = str(port2) + "-" + str(port1)
            tcpinput[4] = 'NULL'
        elif ("-" in user and int(port1) < int(port2)) or not "-" in user:
          if s == "4":
            tcpinput[4] = str(user)
            tcpinput[5] = tcpinput[6] = 'NULL'
          elif s == "5":
            tcpinput[5] = str(user)
            tcpinput[4] = 'NULL'
          elif s == "6":
            tcpinput[6] = str(user)
            tcpinput[4] = 'NULL'
        break
      else:
        print "\n\\\\ERROR: INVALID INPUT - Please enter a valid Port number or range - ERROR: INVALID INPUT//\n\n"
def validate_port(port):
  if "." in port:
    return False
  if "-" in port:
    port1, port2 = port.split("-")
    if not (port1.isdigit() and port2.isdigit()):
      return False
    elif (int(port1) < 0 or int(port1) > 65535) and (int(port2) < 0 or int(port2) > 65535):
      return False
    else:
     return True
  elif not port.isdigit():
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
    if 0 < len(user) <= 2:
      if list(user)[0] in ["1", "2", "3"]: # IP options
        if len(user) == 2 and list(user)[1].lower() == "c": # Clear specified IP option
          tcpinput[int(list(user)[0])] = 'NULL'
        elif user in ["1", "2", "3"]:  
          ip_func(user)
        else:
          print "\n\\\\ERROR: INVALID INPUT - Please enter a valid option - ERROR: INVALID INPUT//\n\n"
      elif list(user)[0] in ["4", "5", "6"]: # Port options
        if len(user) == 2 and list(user)[1].lower() == "c": # Clear specified port option
          tcpinput[int(list(user)[0])] = 'NULL'
        elif user in ["1", "2", "3"]:  
          port_func(user)
        else:
          print "\n\\\\ERROR: INVALID INPUT - Please enter a valid option - ERROR: INVALID INPUT//\n\n"
        
      elif user == "7":
        while True:
          print "\nIf at anytime you want to leave, just enter 'M'\n\nPlease enter a valid absolute directory path for the source directory.\n"
          user = raw_input("Source Directory Path = ")
          if list(user)[0].lower() == "m":
            break
          elif os.path.exists(user):
            tcpinput[0] = user
            break
          else:
            print "\n\\\\ERROR: INVALID INPUT - Please enter a valid absolute directory path - ERROR: INVALID INPUT//\n\n"
      elif user == "8":
        while True:
          print "\nIf at anytime you want to leave, just enter 'M'\n\nPlease enter a valid absolute directory path for the destination directory and filename.\nIf the directory does not exist, the script will create directory path."
          user = raw_input("Destination Directory Path & Filename = ")
          if list(user)[0].lower() == "m":
            break
          elif os.path.exists(user):
            tcpinput[7] = user
            break
          elif not os.path.isdir(user):
            tcpinput[7] = user
            break
          else:
            print "\n\\\\ERROR: INVALID INPUT - Please enter a valid absolute directory path - ERROR: INVALID INPUT//\n\n"
          
      elif str(list(user)[0]).lower() == "c": # Clears all fields
        while True:
          print "\nAre you sure you want to clear all fields? This is irreversable. [Y/N]"
          user = raw_input(">>>")
          if list(user)[0].lower() == "y":
            tcpinput[0] = '/home/' + current_user + '/packets-master/'
            tcpinput[7] = '/tmp/tcpoutput.pcap'
            for i in range(len(tcpinput)):
              if 0 < i < 7:
                tcpinput[i] = 'NULL'
            break
          elif list(user)[0].lower() == "n":
            break
          else:
            print "\n\\\\ERROR: INVALID INPUT - Please only enter [Y/N] - ERROR: INVALID INPUT//\n"
      elif str(list(user)[0]).lower() == "e": # Executes command with current fields
        tcpd_com = "for i in `find " + str(tcpinput[0]) + " -type f` ; do tcpdump -n -r $i" 
        for i in range(len(tcpinput)): # Checks each entry in tcpinput
          if not (i == 0 or i == 7) and not tcpinput[i] == 'NULL': # Skips NULL data
            # IP Data
            if i == 2:
                tcpd_com += " src"
            if i == 3:
              tcpd_com += " dst"
            if not (i == 0 or i == 7) and "/" in list(str(IP(tcpinput[i], make_net=True))): # Network entry checker
              tcpd_com += " net " + str(tcpinput[i])
            elif i in range(1, 4):
              tcpd_com += " host " + str(tcpinput[i])
            # Port Data
            if i == 5:
                tcpd_com += " src"
            if i == 6:
                tcpd_com += " dst"
            if not (i == 0 or i == 7) and "-" in list(str(tcpinput[i])) and i in range(4, 7):
              tcpd_com += " portrange " +str(tcpinput[i])
            elif i in range(4, 7):
              tcpd_com += " port " + str(tcpinput[i])
        
        tcpd_com += " -w /tmp/$i'.tmpdump'; done && mergecap  -w " + str(tcpinput[7]) + " /tmp/*.tmpdump && find -type f -name /tmp/'*tmpdump*' -delete"
        print tcpd_com
        exec(tcpd_com)
      elif list(user)[0].lower() == "q":
          break
      else:
        print "\n\\\\ERROR: INVALID INPUT - Please enter a valid option - ERROR: INVALID INPUT//\n\n"
    else:
      print "\n\\\\ERROR: INVALID INPUT - Please enter a valid option - ERROR: INVALID INPUT//\n\n"
main()
