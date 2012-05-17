#!/usr/bin/env python
import wx,commands,os,subprocess
filepath=""
pid=0
def refresh(event):
	global filepath
	global pid
	if filepath!=pathname.GetValue():
		print "New watch."
		filepath=pathname.GetValue()
		if pid!=0:
			y=os.system("kill %d"%pid)
			if y!=0:
				print "kill %d"%pid,"unsuccessfully!"
		x="/home/heaven/excalibur/ava %s &"%(filepath)
		y=os.system(x)
		if y!=0:
			print "Error during run ava."
		#z=os.popen(x).readlines();
		#z = subprocess.Popen(["/home/heaven/excalibur/test/ava","%s"%filepath,"&"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		#y,z=commands.getstatusoutput(x)
		print "here"
	y=os.system("/home/heaven/excalibur/deallog")
	if y!=0:
		print "Error during run deallog."
	logfile=open("/home/heaven/stdlog.txt","r")
	logtemp=logfile.readlines()
	if logtemp:
		pid=logtemp[0]
		#print "ava pid is",pid
		logtext.SetValue("".join(logtemp[1:]))
	logfile.close()		

fm=wx.App()
face=wx.Frame(None,title="File_Monitor",size=(800,600))
bkg=wx.Panel(face)
refreshbutton=wx.Button(bkg,label='Refresh')
refreshbutton.Bind(wx.EVT_BUTTON,refresh)
pathname=wx.TextCtrl(bkg)
logtext=wx.TextCtrl(bkg,style=wx.TE_MULTILINE|wx.HSCROLL)
hbox=wx.BoxSizer()
hbox.Add(pathname,proportion=1,flag=wx.EXPAND)
hbox.Add(refreshbutton,proportion=0,flag=wx.EXPAND)
vbox=wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
vbox.Add(logtext,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)
bkg.SetSizer(vbox)
face.Show()
fm.MainLoop()
