#!/usr/bin/env python
import os,commands
x=os.getcwd()
info=open(x+'/codeinfo.txt','r')
codeinfo=info.read().split()
if codeinfo[0]=='1000':
  pass
if codeinfo[1]=='cplusplus':
  y,z=commands.getstatusoutput("g++ -o inpro incode.c -Wall")
if y!=0 :
  result=open(x+'/result','w')
  result.write('Compilation Error\n'+z)
  result.close()
  exit()
y,z=commands.getstatusoutput("./inpro < in > out")
if y!=0 :
  result=open(x+'/result','w')
  result.write('Runtime Error\n'+z)
  result.close()
  exit()
testoutfile=open(x+'/out','r')
stdoutfile=open(x+'/stdout','r')
testout=testoutfile.read()
stdout=stdoutfile.read()
if cmp(testout,stdout)==0 :
  result=open(x+'/result','w')
  result.write('Accepted\n')
  result.close()
  exit()
else :
  testcase=testout.split()
  stdcase=stdout.split()
  lenth=len(stdcase)
  waflag=0
  if len(testcase)!=lenth :
    waflag=1
  else :
    for i in xrange(0,lenth) :
       if testcase[i]!=stdcase[i] :
         waflag=1
         break
result=open(x+'/result','w')
if waflag==0 :
  result.write('Presentation Error\n')
else :
  result.write('Wrong Answer\n')
info.close()
result.close()
print 'Done.'
