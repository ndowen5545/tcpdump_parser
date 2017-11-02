# #!/usr/bin/env python
import getpass

current_user = getpass.getuser()
tcpinput = ['/home/' + current_user + '/packets-master/', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', '/tmp/tcpoutput.pcap']
#                              sdir                       specip  specpt    sip    dip     sport   dport           dfile

banner = "\n\n\n          ~~~~~~~~~~~~~~~~~~~~ TCPDUMP PARCER ~~~~~~~~~~~~~~~~~~~~"
def menu_text():
  print """This script is designed to allow tcpdump to parce through multiple PCAP files as 
well as simplify the tcpdump command.

If you do not want to search for a certain field, leave empty.
There is no need to input any data for non-essential fields.
By default, the source file path is the 'packets-master/' directory within 
    the current user's home directory.
By default, the destination file is 'tcpoutput.pcap' in the '/tmp/' directory.

              --------------Current configuration-------------
"""

  print " Source File Path: ", tcpinput[0]
  print "  Dest. File Path: ", tcpinput[7], "\n"
  for i in range(len(tcpinput)):
    if not tcpinput[i] == 'NULL':
      if i == 1:
        print "               IP: ", tcpinput[1]
      elif not i == 1:
        if i == 3:
          print "        Source IP: ", tcpinput[3]
        if i == 4:
          print "   Destination IP: ", tcpinput[4]
      if i == 2:
        print "             Port: ", tcpinput[2]
      elif not i == 2:
        if i == 5:
          print "      Source Port: ", tcpinput[5]
        if i == 6:
          print " Destination Port: ", tcpinput[6]
  print """
              ------------------------------------------------

If a specific IP or port is made, source/destination IPs/ports will be nulled.

Please choose from the following options:
  Modify:
    1) Specific IP          4) Specific Port
    2) Source IP            5) Source Port 
    3) Destination IP       6) Destination Port
    
    7) Source File          8) Destination File
    
  Clear:
    C1) Specific IP          C4) Specific Port
    C2) Source IP            C5) Source Port 
    C3) Destination IP       C6) Destination Port
    
    C7) Source File          C8) Destination File
    
    E) Execute tcpdump with current configuration
    Q) Quit script
"""

def ip_func(s):
    while True:
      print "If at anytime you want to leave, just enter 'M'\n\nPlease put a valid IP address (wildcard '*' accepted)."
      if s == "1":
        user = raw_input("Specific IP = ")
      elif s == "2":
        user = raw_input("Source IP = ")
      elif s == "3":
        user = raw_input("Destination IP = ")
      if user == "M" or user == "m":
        break
      elif validate_ip(user) is False:
        print "ERROR: INVALID INPUT\nPlease input a valid IP address.\n\n"
      elif validate_ip(user) is True:
        if s == "1":
          tcpinput[1] = user
          tcpinput[3] = tcpinput[4] = 'NULL'
        elif s == "2":
          tcpinput[3] = user
          tcpinput[1] = 'NULL'
        elif s == "3":
          tcpinput[4] = user
          tcpinput[1] = 'NULL'
        break
      else:
        print "ERROR: INVALID INPUT\nPlease input a valid IP address.\n\n"
def port_func(s):
  while True:
      print "If at anytime you want to leave, just enter 'M'\n\nPlease input a valid port number."
      if s == "4":
        user = raw_input("Specific Port = ")
      elif s == "5":
        user = raw_input("Source Port = ")
      elif s == "6":
        user = raw_input("Destination Port = ")
      if user == "M" or user == "m":
        break
      elif validate_port(user) is False:
        print "ERROR: INVALID INPUT\nPlease input a valid port number.\n\n"
      elif validate_port(user) is True:
        if s == "4":
          tcpinput[2] = user
          tcpinput[5] = tcpinput[6] = 'NULL'
        elif s == "5":
          tcpinput[5] = user
          tcpinput[2] = 'NULL'
        elif s == "6":
          tcpinput[6] = user
          tcpinput[2] = 'NULL'
        break
      else:
        print "ERROR: INVALID INPUT\nPlease input a valid Port number.\n\n"

def validate_ip(s):
  a = s.split('.')
  if len(a) != 4:
    return False
  for x in a:
    if not x.isdigit() and not x == "*":
      return False
    if not x == "*":
      i = int(x)
      if i < 0 or i > 255:
        return False
    else:
      continue
  return True
def validate_port(s):
  if not s.isdigit():
      return False
  elif int(s) < 0 or int(s) > 65535:
    return False
  else:
    return True

def main():
  while True:
    print banner
    menu_text()
    user = raw_input(">")
    
    if user == "1" or user == "2" or user == "3":
      ip_func(user)
    elif user == "4" or user == "5" or user == "6":
      port_func(user)
    
    #elif user == "7":
      
      
    elif user == "E" or user == "e":
      tcpd_com = "for i in `find " + str(tcpinput[0]) + " -type f` ; do tcpdump -n -r $i" 
      for i in range(len(tcpinput)):
        if not tcpinput[i] == 'NULL':
          if i == 1:
            tcpd_com += " host " + str(tcpinput[1])
          elif not i == 1:
            if i == 3:
              tcpd_com += " src host " + str(tcpinput[3])
            if i == 4:
              tcpd_com += " dst host " + str(tcpinput[4])
          if i == 2:
            tcpd_com += " port " + str(tcpinput[2])
          elif not i == 2:
            if i == 5:
              tcpd_com += " src port " + str(tcpinput[5])
            if i == 6:
              tcpd_com += " dst port " + str(tcpinput[6])
      tcpd_com += " -w /tmp/$i'.tmpdump'; done && mergecap  -w " + str(tcpinput[7]) + " /tmp/*.tmpdump && find -type f -name /tmp/'*tmpdump*' -delete"
      print tcpd_com
    elif user == "Q" or user == "q":
      break
    else:
      print "ERROR: INVALID INPUT\nPlease input a valid option.\n\n"
main()
