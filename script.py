# #!/usr/bin/env python
#from IPy import IP

running = True
tcpinput = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL']
#           sfile   specip  specpt    sip    dip     sport   dport   dfile


banner = "\n\n\n          ~~~~~~~~~~~~~~~~~~~~ Tcpdump Parcer ~~~~~~~~~~~~~~~~~~~~"
menu_text = """This script is designed to allow tcpdump to parce through multiple
PCAP files as well as simplify the tcpdump command.

If you do not want to search for a certain field, leave empty.
There is no need to input any data for non-essential fields.

If a specific IP or port is made, source/destination IPs/ports will be nulled.

Please choose from the following options:
    1)  Specific IP         2)   Specific Port
    1.1) Source IP          2.1) Source Port 
    1.2) Destination IP     2.2) Destination Port
    
    D) Display current input
    
    Q) Quit
"""

def input_error(x):
  if x == False:
    print "ERROR: INVALID INPUT\nPlease input a valid entry.\n\n"
    return False
  else:
    return True

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

def port_val(s):
  if not s.isdigit():
      return False
  else:
    return True
    
def displayer():
  for i in tcpinput:
          if not (tcpinput[i] == 'NULL' or tcpinput[i] == ""):
            if i == 1:
              

#for i in `find /home/soadmin/packets-master/ -type f` ; do tcpdump -n -r $i port 22 -w $i'.tmp'; done && mergecap  -w test3.pcap *.tmp && find -type f -name '*tmp*' -delete
  
def main():
  while running:
    print banner
    print menu_text
    user = raw_input(">")
    
    if int(user) == 1:
      while True:
        print "If at anytime you want to leave, just enter 'M'\n\nPlease put IP in XXX.XXX.XXX.XXX format"
        user = raw_input("Specific IP = ")
        if user == "M" or user == "m":
          break
        elif validate_ip(user) is False:
          input_error(validate_ip(user))
        elif validate_ip(user) is True:
          tcpinput[1] = user
          tcpinput[3] = tcpinput[4] = 'NULL'
          break
        else:
          print "ERROR: INVALID INPUT\nPlease input a valid entry.\n\n"
    elif int(user) == 2:
      while True:
        print "If at anytime you want to leave, just enter 'M'\n"
        user = raw_input("Specific Port = ")
        if user == "M" or user == "m":
          break
        elif port_val(user) is False:
          input_error(port_val(user))
        elif port_val(user) is True:
          tcpinput[2] = user
          break
        else:
          print "ERROR: INVALID INPUT\nPlease input a valid entry.\n\n"
    
    elif user == "D" or user == "d":
      print "\n\nCurrent running configuration:"
      displayer()
      
    elif user == "Q" or user == "q":
      break
main()
