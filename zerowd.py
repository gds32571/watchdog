#!/usr/bin/python
# Echo server program

# gswann Dec 2018
# first in Pace, then rewrittten
# as generic module similar to gtserver.py
# on amd1

# do this to install mosquitto on Pi Zero computer
# sudo apt install mosquitto mosquitto-clients


import pdb
import socket
import paho.mqtt.publish as publish
import sys

#print str(sys.argv)
#print sys.argv[1]


def usage(myCLP):
   print"Value '" + myCLP + "' not in list"
   print"   use 1 for rp5"
   print"   use 2 for sdr"
   print"   use 3 for zero4"
   print"   use 4 for sendtoWU"
   print"   use 5 for gfc"
   print"   use 6 for rp6"
   print"   use 7 for zero5"
   print"   use 8 for rp2"
   print"   use 9 for rp7"
#   print"   use 10 for test"
   print"   use 11 for sdrrp8"
   print"   use 20 for cl-zero4"
   print"   use 21 for cl-rp5"
   print"   use 22 for cl-rp6"
   print"   use 24 for cl-rp7"
   print"   use 23 for cl-rp1"
   print"   use 25 for cl-rp2"
   print"   use 99 for database lookup"


if len(sys.argv) < 2:
   print "no clp"
   usage(' ')
   sys.exit()

#pdb.set_trace()
#print str(sys.argv)

clp = sys.argv[1]

arrPort =     [3001 ,3002 ,3004   ,3005      ,3006 ,3007 ,3008   ,3009 ,3011 ,3050 ,3012    ,3020     ,3021   ,3022   ,3023   ,3024   ,3025   ,3026    , 2999]
arrName =     ["rp5","sdr","zero4","sendtoWU","gfc","rp6","zero5","rp2","rp7","rp8","sdrrp8","clzero4","clrp5","clrp6","clrp1","clrp7","clrp2","clrp8" , "database"]
arrDatatype = ['1'  ,'2'  ,'3'    ,'4'       ,'5'  ,'6'  ,'7'    ,'8'  ,'9'  ,'10' ,'11'    ,'20'     ,'21'   ,'22'   ,'23'   ,'24'   ,'25'   ,'26'    ,'99']
arrTimer =    [60   ,90   ,60     ,130       ,65   ,60   ,95     ,60   ,60   ,60   ,90      ,205      ,205    ,205    ,205    ,205    ,205    ,205     ,180 ]

try:
   datatype = arrDatatype.index(clp)
except:
   usage(clp)
   sys.exit()

srvName = arrName[datatype]
myTimeout = arrTimer[datatype] + 15.0
PORT = arrPort[datatype]

print "listening for " + srvName + " on port " + str(PORT) + " with timer = " + str(myTimeout)
 
hassHost = "192.168.2.6"
ctr = 0
HOST = ''                # Symbolic name meaning all available interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.settimeout(myTimeout) 
s.listen(2)

timeouts = 0;
connects = 0;

#pdb.set_trace()

while True:
 try:
  conn, addr = s.accept()
  connects += 1
  myStr = 'Connection ' + str(ctr) + ' from ' + str(addr) + '(' + srvName + '-' + str(PORT)+ ') ' + str(timeouts) + "/" + str(connects) 
  print myStr
  while True:
    data = conn.recv(1024)

    if data=='reset':
       timeouts = 0
       connects = 0
       ctr = -1
       print data
   
    elif 'host' in data:
       print(data)
       myhost=data[4:]
       print(myhost)

       myindex=arrName.index(myhost)
       myport=arrPort[myindex]

       print("assigning port: " + str(myport))

       conn.sendall('reply ' + str(myport)  )

    else:       

       ctr += 1
       conn.sendall('reply ' +   str(ctr)  )

       try:
          publish.single(srvName + "/apprunning" , "yes" , hostname=hassHost, auth = {'username':"hass", 'password':"hass"})
       except:
         print("Couldn't publish " + srvName + "/apprunning")
       break



 except KeyboardInterrupt:
    print('keyboard interrupt %s')
    exit()
 except:
    timeouts += 1
    print('timeout ' + srvName )
    try:
      publish.single(srvName + "/apprunning" , "no" , hostname=hassHost, auth = {'username':"hass", 'password':"hass"})
    except:
      print("Couldn't publish " + srvName + "/apprunning")

conn.close()
              
