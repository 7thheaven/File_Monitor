#!/usr/bin/env python
logfile=open("/home/heaven/stdlog.txt","r")
logtemp=logfile.readlines()
if logtemp:
	pid=logtemp[0]
	print "ava pid is",pid
	print ("".join(logtemp[1:]))
logfile.close()
