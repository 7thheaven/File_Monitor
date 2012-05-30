#!/usr/bin/env python
import wx,commands,os,subprocess
import wx.grid
filepath=""
pid=0
rownum=0
colLabels=("Filename","Event","Relates","Processname","Time")
def refresh(event):
	global filepath
	global pid
	if filepath!=pathname.GetValue():
		print "New watch."
		filepath=pathname.GetValue()
		if pid!=0:
			y=os.system("kill %s"%pid)
			if y!=0:
				print "kill %s unsuccessfully!"%pid
			else:
				print "kill %s Done."%pid
				pid=0
				filepath=""
		x="/home/heaven/excalibur/ava %s &"%(filepath)
		y=os.system(x)
		if y!=0:
			print "Error during run ava."
		#z=os.popen(x).readlines();
		#z = subprocess.Popen(["/home/heaven/excalibur/test/ava","%s"%filepath,"&"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		#y,z=commands.getstatusoutput(x)
		#print "here"
	y=os.system("/home/heaven/excalibur/deallog")
	if y!=0:
		print "Error during run deallog."
	logfile=open("/home/heaven/stdlog.txt","r")
	logtemp=logfile.readlines()
	#if logtemp:
	#	pid=logtemp[0]
	#	print "ava pid is",pid
	#	logtext.SetValue("".join(logtemp[1:]))
	global colLabels
	global rownum
	pos=face.GetSize()
	for col in xrange(5):
		reslog.SetColLabelValue(col,colLabels[col])
		reslog.SetColSize(col,(pos.x-85)/5)
	if logtemp:
		pid=logtemp[0]
		print "ava pid is",pid
		rownum=len(logtemp)-1
		for row in xrange(rownum):
			for col in xrange(5):
				if col==4:
					reslog.SetCellValue(row, col, "%s" % " ".join(logtemp[row+1].split()[col:]))
				else:
					reslog.SetCellValue(row, col, "%s" % (logtemp[row+1].split()[col]))
	face.Refresh()
	logfile.close()

def clear(event):
	global pid
	global rownum
	if pid!=0:
		y=os.system("kill %s"%pid)
		if y!=0:
			print "kill %s unsuccessfully!"%pid
		else:
			print "kill %s Done."%pid
			pid=0
			filepath=""
			for row in xrange(rownum):
				for col in xrange(5):
					reslog.SetCellValue(row, col,"")	

def browser(event):
	global filepath
	dlg=wx.DirDialog(bkg,u"select",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
	if dlg.ShowModal() == wx.ID_OK:
		path=dlg.GetPath()
		pathname.SetValue(path+"/")

fm=wx.App()
face=wx.Frame(None,title="File_Monitor",size=(800,600))
bkg=wx.Panel(face)
browserbutton=wx.Button(bkg,label='Browser')
browserbutton.Bind(wx.EVT_BUTTON,browser)
refreshbutton=wx.Button(bkg,label='Refresh')
refreshbutton.Bind(wx.EVT_BUTTON,refresh)
clearbutton=wx.Button(bkg,label='Clear')
clearbutton.Bind(wx.EVT_BUTTON,clear)
pathname=wx.TextCtrl(bkg)
proname=wx.TextCtrl(bkg)
#logtext=wx.TextCtrl(bkg,style=wx.TE_MULTILINE|wx.HSCROLL)             
reslog=wx.grid.Grid(bkg)
pos=face.GetSize()
reslog.CreateGrid(1000,5)
for col in xrange(5):
	reslog.SetColLabelValue(col,colLabels[col])
	reslog.SetColSize(col,(pos.x-85)/5)
hbox1=wx.BoxSizer()
hbox2=wx.BoxSizer()
hbox1.Add(pathname,proportion=1,flag=wx.EXPAND)
hbox2.Add(proname,proportion=1,flag=wx.EXPAND)
hbox1.Add(browserbutton,proportion=0,flag=wx.EXPAND)
hbox1.Add(refreshbutton,proportion=0,flag=wx.EXPAND)
hbox2.Add(clearbutton,proportion=0,flag=wx.EXPAND)
vbox=wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox1,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
vbox.Add(hbox2,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
#vbox.Add(logtext,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)
vbox.Add(reslog,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
bkg.SetSizer(vbox)
face.Show()
fm.MainLoop()
